from grld.net_commands import get_coroutines

class GetCoroutinesCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        coroutines = get_coroutines()

        lua_execution_state.coroutines = coroutines

        return debugger_state