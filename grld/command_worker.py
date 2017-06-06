import threading
import time

from shared_data import command_queue, debugger_state_update_queue, ui_debugger_state, unhandled_grld_push_command_queue

class CommandWorker(threading.Thread):
    def run():
        # TODO: don't even allow this to run if we're not connected?
        
        while True:
            # TODO: error handling

            with ui_debugger_state:
                debugger_state = ui_debugger_state.clone()

            command = command_queue.get_nowait()
            if command:
                modified_debugger_state = command.execute(working_debugger_state)

            unhandled_grld_push_command = unhandled_grld_push_command_queue.get_nowait()
            if unhandled_grld_push_command:
                modified_debugger_state = unhandled_grld_push_command.execute(modified_debugger_state)

            debugger_state_update_queue.put(modified_debugger_state)

            time.sleep(0.1)

