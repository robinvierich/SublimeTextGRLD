from grld.path_helpers import get_local_path

from grld.net_commands import get_stack
from grld.state.lua_stack import create_lua_stack, push_stack_frame
from grld.state.lua_stack_frame import create_lua_stack_frame

class GetStackCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        lua_execution_state = debugger_state['lua_execution_state']

        stack_data_response = get_stack(lua_execution_state['current_thread'])

        min_stack_level = None
        new_stack = create_lua_stack()
        for stack_level_str, stack_frame_data in stack_data_response:
            stack_level = int(stack_level_str)
            local_file_path = get_local_path(stack_frame_data["source"])
            lineno = int(stack_frame_data["line"])
            what = stack_frame_data["what"]
            name = stack_frame_data.get('name', None)
            namewhat = stack_frame_data.get('namewhat', None)

            min_stack_level = min(min_stack_level, stack_level)

            stack_frame = create_lua_stack_frame(local_file_path, lineno, what, name, namewhat stack_level)
            push_stack_frame(new_stack, stack_frame)

        lua_execution_state['stack'] = new_stack

        if not lua_execution_state['current_stack_level']:
            lua_execution_state['current_stack_level'] = min_stack_level

        return debugger_state