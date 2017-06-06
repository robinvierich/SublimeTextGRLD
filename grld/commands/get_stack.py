from grld.path_helpers import get_local_path

from grld.net_commands import get_stack
from grld.lua_stack import LuaStack
from grld.lua_stack_frame import LuaStackFrame

class GetStackCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        lua_execution_state = debugger_state.lua_execution_state

        stack_data_response = get_stack(lua_execution_state.current_thread)

        min_stack_level = None
        new_stack = LuaStack()
        for stack_level_str, stack_frame_data in stack_data_response:
            stack_level = int(stack_level_str)
            local_file_path = get_local_path(stack_frame_data["source"])
            lineno = int(stack_frame_data["line"])
            what = stack_frame_data["what"]

            min_stack_level = min(min_stack_level, stack_level)

            stack_frame = LuaStackFrame(local_file_path, lineno, what, stack_level)
            new_stack.push_stack_frame(stack_frame)

        lua_execution_state.stack = new_stack

        if not lua_execution_state.current_stack_level:
            lua_execution_state.current_stack_level = min_stack_level

        return debugger_state