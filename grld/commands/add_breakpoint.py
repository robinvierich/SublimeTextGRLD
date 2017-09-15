from grld.net_commands import add_breakpoint
from grld.state.breakpoint import create_breakpoint

class AddBreakpointCommand:
    def __init__(self, local_path, lineno):
        self.breakpoint = create_breakpoint(local_path, lineno)

    def execute(self, debugger_state):
        add_breakpoint(self.breakpoint['local_path'], self.breakpoint['lineno'])
        debugger_state['breakpoints'].append(self.breakpoint)

        return debugger_state