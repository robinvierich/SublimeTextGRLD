class LuaStackFrame:
    def __init__(self, local_source_file_path, lineno, what, stack_level):
        self.local_source_file_path = local_source_file_path
        self.lineno = lineno
        self.what = what
        self.stack_level = stack_level