from grld.net_commands import add_breakpoint
from grld.breakpoint import Breakpoint

class AddBreakpointCommand:
    def __init__(self, local_path, lineno):
        self.breakpoint = Breakpoint(local_path, lineno)

    def execute(self, debugger_state):
        add_breakpoint(self.breakpoint.local_path, self.breakpoint.lineno)
        debugger_state.breakpoints.append(self.breakpoint)

        return debugger_state