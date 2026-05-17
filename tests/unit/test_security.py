import pytest
import aiosqlite
import os
import base64
from cryptography.fernet import Fernet
from core.config import settings
from core.security.crypto import encrypt, decrypt
from core.intelligence.context_engine import ContextEngine
from core.hybrid.action_logger import ActionLogger

# Setup a valid ENCRYPTION_KEY for tests
@pytest.fixture(autouse=True)
def setup_encryption_key():
    # Generate a fresh 32-byte url-safe base64 key
    key = Fernet.generate_key().decode('utf-8')
    settings.ENCRYPTION_KEY = key
    yield
    settings.ENCRYPTION_KEY = ""

def test_crypto_round_trip():
    """Test that encryption and decryption are symmetric."""
    original_data = "This is a secret step description!"
    encrypted = encrypt(original_data)
    
    assert encrypted != original_data
    assert original_data not in encrypted
    
    decrypted = decrypt(encrypted)
    assert decrypted == original_data

def test_crypto_none_handling():
    """Test encrypt/decrypt handle None properly."""
    assert encrypt(None) is None
    assert decrypt(None) is None

@pytest.mark.asyncio
async def test_context_engine_encryption(tmp_path):
    """Test ContextEngine writes encrypted data and reads it back as plaintext."""
    db_path = str(tmp_path / "test_execra.db")
    engine = ContextEngine(db_path=db_path)
    
    session_id = await engine.create_session("digital")
    secret_desc = "Super secret screen content: user email is admin@example.com"
    await engine.update_step(session_id, 1, secret_desc)
    
    # Verify raw DB value is NOT plaintext
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT step_description FROM session_context WHERE session_id = ?", (session_id,)) as cursor:
            row = await cursor.fetchone()
            raw_db_value = row[0]
            assert raw_db_value != secret_desc
            assert "admin@example.com" not in raw_db_value
    
    # Verify transparent decryption on read
    context = await engine.get_context(session_id)
    assert context is not None
    assert context["step_description"] == secret_desc

@pytest.mark.asyncio
async def test_action_logger_encryption(tmp_path):
    """Test ActionLogger writes encrypted error data and reads it back as plaintext."""
    db_path = str(tmp_path / "test_execra.db")
    logger = ActionLogger(db_path=db_path)
    
    session_id = "test-session-123"
    secret_error = "Exception in auth module: password '123456' rejected"
    await logger.log_error(session_id, 1, secret_error)
    
    # Verify raw DB value is NOT plaintext
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT error FROM error_history WHERE session_id = ?", (session_id,)) as cursor:
            row = await cursor.fetchone()
            raw_db_value = row[0]
            assert raw_db_value != secret_error
            assert "123456" not in raw_db_value
            
    # Verify transparent decryption on read
    errors = await logger.get_errors(session_id)
    assert len(errors) == 1
    assert errors[0]["error"] == secret_error
