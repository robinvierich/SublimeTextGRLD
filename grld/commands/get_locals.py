from grld.net_commands import get_locals
from grld.breakpoint import Breakpoint

class GetLocalsCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        lua_execution_state = debugger_state.lua_execution_state

        locals = get_locals(self.lua_execution_state.current_thread, self.lua_execution_state.current_stack_level)

        lua_execution_state.locals = locals

        return debugger_state