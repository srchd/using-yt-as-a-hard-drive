from typing import Any

class Observable:
    def __init__(self, initial_value) -> None:
        self.data = initial_value
        self.callbacks = {}

        return

    def add_callback_function(self, func) -> None:
        self.callbacks[func] = 1

        return
    
    def remove_callback_function(self, func) -> None:
        del self.callbacks[func]

        return
    
    def _do_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.data)

        return
    
    def set(self, data) -> None:
        self.data = data
        self._do_callbacks()

        return

    def set_without_callback(self, data) -> None:
        self.data = data

    def get(self) -> Any:
        return self.data
    
    def unset(self) -> None:
        self.data = None

        return
