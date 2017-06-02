import threading

from lua_execution_state import LuaExecutionState

def assert_not_locked(func):
    def wrapper(self, *args, **kwargs):
        assert self.is_locked(), "Cannot access DebuggerState outside of a with statement! This is to ensure thread safety."
        return func(self, *args, **kwargs)

class DebuggerState:
    def __init__(self, lua_execution_state=None):
        self.breakpoints = []
        self.watch_expressions = []

        self.rlock = threading.RLock()
        self.locked = 0

        self.lua_execution_state = lua_execution_state or LuaExecutionState()

    def is_locked(self):
        return self.locked > 0

    # TODO: this is slow, probably just lock access to the global instance
    @assert_locked
    def __getattribute__(self, arg):
        return super().__getattribute__(arg)

    @assert_locked
    def __setattr__(self, arg, value):
        return super().__setattr__(arg, value)

    def __enter__(self):
        self.rlock.acquire()
        self.locked += 1
        return self

    def __exit__(self, err_type, error_obj, traceback):
        self.rlock.release()
        self.locked = max(self.locked - 1, 0)


global_debugger_state = DebuggerState()