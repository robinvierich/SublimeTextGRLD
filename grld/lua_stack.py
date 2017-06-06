class LuaStack:
    def __init__(self):
        # {stack_level: stack_frame}
        self.stack_frames = {}

    def push_stack_frame(self, stack_frame):
        stack_level = stack_frame.stack_level

        self.stack_frames[stack_level] = stack_frame