from grld.net_commands import step_over

class StepOverCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        step_over()
        return debugger_state