from lua_stack import LuaStack

class RunningState:
    RUNNING = 0
    PAUSED = 1

class LuaExecutionState:
    def __init__(self):

        self.running_state = RunningState.RUNNING

        self.current_thread = None
        self.current_stack_level = None

        self.stack = LuaStack()
        self.coroutines = []

        self.locals = []
        self.upvalues = []
        
    def get_current_stack_frame(self):
        if not self.stack: return None
        if not self.current_stack_level: return None

        return self.stack.stack_frames[self.current_stack_level]