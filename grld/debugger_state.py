import time

from breakpoint import Breakpoint
from lua_execution_state import LuaExecutionState

class DebuggerState:
    def __init__(self, lua_execution_state=None):
        self.connected = False
        self.last_break_time = None

        self.breakpoints = []
        self.watch_expressions = []

        #TODO: clear out this list periodically
        self.evaluated_expressions = {}

        self.lua_execution_state = lua_execution_state or LuaExecutionState()

    def add_evaluated_expression_response(self, expression, thread, stack_level, response):
        curr_time = time.clock()
        self.evaluated_expressions[(expression, thread, stack_level, curr_time)] = response


    def does_breakpoint_exist(self, local_path, lineno):
        breakpoint = Breakpoint(local_path, lineno)
        return (breakpoint in self.breakpoints)