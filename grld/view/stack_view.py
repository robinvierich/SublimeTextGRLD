class StackView:
    def __init__(self, settings):
        pass

    # on click

    def __get_stack_frame_line(self, stack_frame):
        return str.format('[{stack_level}] {local_source_file_path}:{lineno} - {name}({namewhat})', stack_frame)

    def get_contents(self, debugger_state):
        lua_execution_state = debugger_state['lua_execution_state']

        stack = lua_execution_state['stack']

        content_lines = (self.__get_stack_frame_line(stack_frame) for (stack_level, stack_frame) in stack['stack_frames'])

        return "\n".join(content_lines)