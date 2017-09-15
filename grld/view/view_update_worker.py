import threading
import time

from shared_data import debugger_state_update_queue, safe_update_debugger_state

class ViewUpdateWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.views = []
        self.__stop = False
        return super().__init__(*args, **kwargs)

    def add_view(self, view):
        pass

    def remove_view(self, view):
        pass

    def stop(self):
        self.__stop = True

    def run(self):
        while not self.__stop:
            debuger_state_update = debugger_state_update_queue.get_nowait()
            if debuger_state_update:
                safe_update_debugger_state(debuger_state_update)

                debugger_state = get_immutable_debugger_state()

                for view in self.views:
                    view.update(debugger_state)

            time.sleep(0.1)



