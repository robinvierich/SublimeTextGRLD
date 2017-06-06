from grld.net_commands import step_out

class StepOutCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        step_out()
        return debugger_state