class ContextView:
    def __init__(self, settings):
        pass

    def get_contents(self, debugger_state):
        content_lines = (self.__get_breakpoint_line(breakpoint) for breakpoint in debugger_state['breakpoints'])

        return "\n".join(content_lines)