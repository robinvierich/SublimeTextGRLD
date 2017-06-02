import queue
import threading

class SynchronizedDict:
    def __init__(self):
        self.lock = threading.Lock()
        self._dict = {}

    def set(self, key, value):
        self.lock.acquire()
        self._dict[key] = value
        self.lock.release()

    def get(self, key):
        self.lock.acquire()
        val = self._dict[key]
        self.lock.release()
        return val

command_queue = queue.Queue()

#net_read_queue = queue.Queue()
#net_write_queue = queue.Queue()

net_request_transaction_queue = queue.Queue()

unhandled_responses = SynchronizedDict()
unhandled_grld_push_command_queue = queue.Queue()

ui_update_queue = queue.Queue()


