from grld.net_commands import step_in

class StepInCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        step_in()
        return debugger_state