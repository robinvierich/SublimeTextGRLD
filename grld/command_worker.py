import threading
import time

from shared_collections import command_queue

class CommandWorker(threading.Thread):
    def run():
        # TODO: don't even allow this to run if we're not connected?
        
        while True:
            # TODO: error handling
            command = command_queue.get()
            command_fn(*args)

            time.sleep(0.1)

        



