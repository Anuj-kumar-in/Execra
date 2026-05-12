from typing import Callable

class ModeManager:
    
    def __init__(self):
        self.current_mode = "passive"
        self._callbacks = []

    def switch_mode(self,mode: str):
        VALID_MODES = ["passive", "active", "mixed"]

        if mode not in VALID_MODES:
            raise ValueError(f"Invalid mode '{mode}'. Choose from: {VALID_MODES}")
        
        self.current_mode = mode
        self._notify_observers()

    def get_current_mode(self) -> dict:
        descriptions = {
            "passive": "Execra is observing and guiding automatically. No prompts needed.",
            "active": "Switched to Active Mode. You can now ask questions.",
            "mixed": "Execra is observing automatically while also accepting your questions."
        }

        return {
            "mode": self.current_mode,
            "description": descriptions[self.current_mode]
        }
    
    def on_mode_change(self, callback: Callable):
        self._callbacks.append(callback)

    def _notify_observers(self):
        for callback in self._callbacks:
            callback(self.current_mode)

# Singleton instance of ModeManagerdone
mode_manager = ModeManager()