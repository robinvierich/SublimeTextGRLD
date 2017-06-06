from grld.net_commands import resume

class ResumeCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        resume()
        return debugger_state