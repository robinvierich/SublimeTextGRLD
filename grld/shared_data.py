import queue
import threading

from grld.state.debugger_state import create_debugger_state

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

# a queue of commands from the UI
command_queue = queue.Queue()

# a queue of network transations to complete
net_request_transaction_queue = queue.Queue()

# a queue of data pushed/returned from the GRLD client (i.e. the game/application running Lua)
unhandled_responses = SynchronizedDict()
unhandled_grld_push_command_queue = queue.Queue()

# a queue of updates to the debugger state
debugger_state_update_queue = queue.Queue()

# the main debugger state of the application
debugger_state = create_debugger_state()