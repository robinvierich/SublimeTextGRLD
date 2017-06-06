from grld.commands.get_coroutines import GetCoroutinesCommand

from grld.net_commands import get_current_thread

class GetCurrentThreadCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        get_coroutines_command = GetCoroutinesCommand()
        debugger_state_with_latest_coroutines = get_coroutines_command.execute(debugger_state)

        current_thread = get_current_thread()

        selected_coroutine = None

        for coroutine in debugger_state_with_latest_coroutines.lua_execution_state.coroutines:
            if coroutine.id == current_thread:
                selected_coroutine = coroutine
                break

        if not selected_coroutine:
            selected_coroutine = 'main'

        debugger_state_with_latest_coroutines.lua_execution_state.current_thread = selected_coroutine

        return debugger_state_with_latest_coroutines