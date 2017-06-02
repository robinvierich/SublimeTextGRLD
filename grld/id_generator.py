from threading import Lock

class IdGenerator:
    def __init__(self, formatFn=None, initialValue=0):
        self.update_lock = Lock()
        self.id = initialValue
        self.formatFn = formatFn

    def get_next_id():
        self.update_lock.acquire()
        self.id += 1
        self.update_lock.release()

        if self.formatFn:
            yield self.formatFn(self.id)
        else:
            yield self.id