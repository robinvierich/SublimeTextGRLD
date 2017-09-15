class BreakpointsView:
    def __init__(self, settings):
        pass

    # on click

    def __get_breakpoint_line(self, breakpoint):
        return str.format('[{stack_level}] {filename}:{lineno} - {name}({namewhat})', breakpoint)

    def get_contents(self, debugger_state):
        content_lines = (self.__get_breakpoint_line(breakpoint) for breakpoint in debugger_state['breakpoints'])

        return "\n".join(content_lines)