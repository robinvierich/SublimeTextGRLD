import time

from grld.path_helpers import get_local_path

from grld.commands.get_coroutines import GetCoroutinesCommand
from grld.commands.get_stack import GetStackCommand
from grld.commands.get_upvalues import GetUpvaluesCommand
from grld.commands.get_locals import GetLocalsCommand

from grld.shared_data import command_queue


class BreakPushCommandHandler:
    def __init__(self):
        pass

    def handle(self, debugger_state, grld_file_path, lineno):

        debugger_state['last_break_time'] = time.clock()
        #lua_execution_state = debugger_state['lua_execution_state']
        #lua_execution_state['current_local_file_path'] = get_local_path(grld_file_path)
        #lua_execution_state['current_lineno'] = lineno

        command_queue.put(GetCoroutinesCommand())
        command_queue.put(GetStackCommand())
        command_queue.put(GetLocalsCommand())
        command_queue.put(GetUpvaluesCommand())

        return debugger_state