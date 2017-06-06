class Breakpoint:
    def __init__(self, local_path, lineno):
        self.local_path = local_path
        self.lineno = lineno

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return (not self == other)