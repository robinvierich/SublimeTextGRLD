def create_lua_stack():
    return {
        # {stack_level: stack_frame}
        'stack_frames': {}
    }

def push_stack_frame(lua_stack, stack_frame):
    stack_level = stack_frame['stack_level']

    lua_stack['stack_frames'][stack_level] = stack_frame