from grld.state.lua_stack import create_lua_stack

class RunningState:
    RUNNING = 0
    PAUSED = 1

def create_lua_execution_state():
    return {
        'running_state': RunningState.RUNNING,

        'current_thread': None,
        'current_stack_level': None,

        'stack': create_lua_stack(),
        'coroutines': [],

        'locals': [],
        'upvalues': [],
    }


def get_current_stack_frame(lua_execution_state):
    if not lua_execution_state['stack']: return None
    if not lua_execution_state['current_stack_level']: return None

    return lua_execution_state['stack']['stack_frames'][lua_execution_state['current_stack_level']