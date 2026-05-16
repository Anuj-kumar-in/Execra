import pytest
from core.hybrid.mode_manager import ModeManager

@pytest.fixture
def manager():
    return ModeManager()

def test_default_mode_is_passive(manager):
    assert manager.current_mode == "passive"

def test_switch_to_valid_mode(manager):
    manager.switch_mode("active")
    assert manager.current_mode == "active"

def test_switch_to_invalid_mode_raises_error(manager):
    with pytest.raises(ValueError):
        manager.switch_mode("invalid_modedo")

def test_callback_is_called_on_mode_change(manager):
    results = []

    def my_callback(new_mode):
        results.append(new_mode)

    manager.on_mode_change(my_callback)
    manager.switch_mode("active")

    assert results == ["active"]


def test_multiple_callbacks_all_fire(manager):
    results = []

    def callback_one(mode):
        results.append("one")

    def callback_two(mode):
        results.append("two")

    manager.on_mode_change(callback_one)
    manager.on_mode_change(callback_two)
    manager.switch_mode("mixed")

    assert len(results) == 2
    assert "one" in results
    assert "two" in results


def test_get_current_mode_returns_mode_and_description(manager):
    result = manager.get_current_mode()

    assert result["mode"] == "passive"
    assert "description" in result
    assert isinstance(result["description"], str)

def test_description_changes_with_mode(manager):
    manager.switch_mode("active")
    result = manager.get_current_mode()

    assert result["mode"] == "active"
    assert result["description"] != ""
    