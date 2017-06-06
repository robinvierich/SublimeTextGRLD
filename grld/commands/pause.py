from grld.net_commands import pause

class PauseCommand:
    def __init__(self):
        pass

    def execute(self, debugger_state):
        pause()
        return debugger_state