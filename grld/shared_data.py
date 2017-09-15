import queue
import threading
import copy

from grld.state.debugger_state import create_debugger_state

from types import MappingProxyType

class SynchronizedDict(dict):
    def __init__(self, *args, **kwargs):
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
unhandled_responses_sync_dict = SynchronizedDict()
unhandled_grld_push_command_queue = queue.Queue()

# a queue of updates to the debugger state
debugger_state_update_queue = queue.Queue()

# the main debugger state of the application
__debugger_state = create_debugger_state()
__debugger_state_lock = threading.Lock()

def safe_update_debugger_state(updates):
    with __debugger_state_lock:
        __debugger_state.update(updates)

def copy_debugger_state():
    with __debugger_state_lock:
        return copy.deepcopy(__debugger_state)

def get_immutable_debugger_state():
    with __debugger_state_lock:
        return MappingProxyType(__debugger_state)

