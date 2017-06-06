from grld.net_commands import get_upvalues

class GetUpvaluesCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        lua_execution_state = debugger_state.lua_execution_state

        upvalues = get_upvalues(lua_execution_state.current_thread, lua_execution_state.current_stack_level)

        lua_execution_state.upvalues = upvalues

        return debugger_state