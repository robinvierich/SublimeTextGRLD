import threading
import time

from shared_data import command_queue, debugger_state_update_queue, copy_debugger_state, unhandled_grld_push_command_queue

class CommandWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def run():
        # TODO: don't even allow this to run if we're not connected?

        while True:
            # TODO: error handling
            debugger_state_updates = None

            command = command_queue.get_nowait()
            if command:
                # TODO: this currently only works because net_commands block.
                #       For perf, it'd be better to have async net requests eventually

                debugger_state_updates = copy_debugger_state()
                debugger_state_updates = command.execute(debugger_state)

            unhandled_grld_push_command = unhandled_grld_push_command_queue.get_nowait()
            if unhandled_grld_push_command:
                debugger_state_updates = unhandled_grld_push_command.execute(debugger_state_updates)

            if debugger_state_updates:
                debugger_state_update_queue.put(debugger_state_updates)

            time.sleep(0.1)

