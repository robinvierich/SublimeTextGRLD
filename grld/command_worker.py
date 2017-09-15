import threading
import time

from copy import deepcopy

from shared_data import command_queue, debugger_state_update_queue, debugger_state, unhandled_grld_push_command_queue

class CommandWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def run():
        # TODO: don't even allow this to run if we're not connected?

        while True:
            # TODO: error handling

            with debugger_state:
                debugger_state = deepcopy(debugger_state)

            command = command_queue.get_nowait()
            if command:
                # TODO: this currently only works because net_commands block.
                #       For perf, it'd be better to have async net requests eventually
                modified_debugger_state = command.execute(working_debugger_state)

            unhandled_grld_push_command = unhandled_grld_push_command_queue.get_nowait()
            if unhandled_grld_push_command:
                modified_debugger_state = unhandled_grld_push_command.execute(modified_debugger_state)

            debugger_state_update_queue.put(modified_debugger_state)

            time.sleep(0.1)

