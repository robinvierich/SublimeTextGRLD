import time

from grld.state.breakpoint import create_breakpoint
from grld.state.lua_execution_state import create_lua_execution_state

from state.dict_wrapper import DictWrapper

def create_debugger_state(self, lua_execution_state):
    return {
        'connected': False,
        'last_break_time': None,
        'breakpoints': []
        'watch_expressions': []

        #TODO: clear out this list periodically
        'evaluated_expressions': {}
        'lua_execution_state': lua_execution_state or create_lua_execution_state()
    }

def add_evaluated_expression_response(debugger_state):
    curr_time = time.clock()
    debugger_state['evaluated_expressions'][(expression, thread, stack_level, curr_time)] = response

def does_breakpoint_exist(debugger_state, local_path, lineno):
    breakpoint = create_breakpoint(local_path, lineno)
    return (breakpoint in debugger_state['breakpoints'])