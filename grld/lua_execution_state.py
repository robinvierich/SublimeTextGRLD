class RunningState:
    RUNNING = 0
    PAUSED = 1

class LuaExecutionState:
    def __init__(self):

        self.running_state = RunningState.RUNNING

        self.current_thread = current_thread = None
        self.current_stack_level = current_stack_level = None

        self.locals = []
        self.upvalues = []

        self.coroutines = []