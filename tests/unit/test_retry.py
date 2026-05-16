import asyncio
import pytest
import unittest

from unittest.mock import Mock, AsyncMock,patch
from openai import APIError, RateLimitError

from core.utils.retry import retry

class TestRetry(unittest.TestCase):

    def test_non_retryable_exception(self):
        
        mock_func = Mock(side_effect=ValueError("invalid input"))
        decorator = retry()(mock_func)

        with pytest.raises(ValueError):
            decorator()

        assert mock_func.call_count == 1


    def test_sync_success_without_retry(self):

        mock_func = Mock(return_value="success")
        decorator = retry()(mock_func)
        result = decorator()

        assert result == "success"
        assert mock_func.call_count == 1

    def test_sync_retries_then_success(self):

        mock_func = Mock(
            side_effect=[
                APIError("temporary error", request=None, body=None),
                "success"
            ]
        )
        decorator = retry(max_retries=3, base_delay=0)(mock_func)
        
        with patch("time.sleep") as mock_sleep:
            
            result = decorator()

            assert result == "success"
            assert mock_func.call_count == 2
            mock_sleep.assert_called_once_with(0)

    def test_sync_max_retries_exceeded(self):

        mock_func = Mock(
            side_effect=(
                APIError("temporary error", request=None, body=None)
            )
        )
        decorator = retry(max_retries=3, base_delay=0)(mock_func)
        
        with patch("time.sleep") as mock_sleep:

            with pytest.raises(APIError):
                decorator()

            assert mock_func.call_count == 3
            assert mock_sleep.call_count == 2
    
    @pytest.mark.asyncio
    async def test_async_success_without_retry(self):

        mock_func = AsyncMock(return_value="success")
        decorator = retry()(mock_func)
        result = await decorator()

        assert result == "success"
        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_async_retries_then_success(self):

        mock_response = Mock()
        mock_response.request = Mock()

        mock_func = AsyncMock(
            side_effect=[
                RateLimitError("temporary error", response=mock_response, body=None),
                "success"
            ]
        )
        decorator = retry(max_retries=3, base_delay=0)(mock_func)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            
            result = await decorator()

            assert result == "success"
            assert mock_func.call_count == 2
            mock_sleep.assert_awaited_once_with(0)

    @pytest.mark.asyncio
    async def test_async_max_retries_exceeded(self):

        mock_response = Mock()
        mock_response.request = Mock()

        mock_func = AsyncMock(
            side_effect=[
                RateLimitError("temporary error", response=mock_response, body=None)
            ]
        )

        decorator = retry(max_retries=3, base_delay=0)(mock_func)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:

            with pytest.raises(RateLimitError):
                await decorator()

            assert mock_func.call_count == 3
            assert mock_sleep.call_count == 2

    def test_exponential_backoff_sync(self):

        mock_response = Mock()
        mock_response.request = Mock()

        mock_func = Mock(
            side_effect=[
                APIError("error1", request=None, body=None),
                RateLimitError("error2", response=mock_response, body=None),
                "success"
            ]
        )
        decorator = retry(max_retries=3, base_delay=1)(mock_func)

        with patch("time.sleep") as mock_sleep:
            decorator()

            assert mock_sleep.call_args_list == [ ((1,),), ((2,),) ]

    @pytest.mark.asyncio
    async def test_exponential_backoff_async(self):

        mock_response = Mock()
        mock_response.request = Mock()

        mock_func = AsyncMock(
            side_effect=[
                APIError("error1", request=None, body=None),
                RateLimitError("error2", response=mock_response, body=None),
                "success"
            ]
        )
        decorator = retry(max_retries=3, base_delay=1)(mock_func)
        
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await decorator()

            assert mock_sleep.call_args_list == [ ((1,),), ((2,),) ]

