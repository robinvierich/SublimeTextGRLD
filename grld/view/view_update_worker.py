from shared_data import debugger_state_update_queue, debugger_state

class ViewUpdateWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


    def run():
        while True:
            modified_debugger_state = debugger_state_update_queue.get_nowait()
            if modified_debugger_state:
