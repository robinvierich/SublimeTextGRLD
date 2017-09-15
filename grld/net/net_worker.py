import time

from grld.shared_data import net_request_transaction_queue, unhandled_grld_push_command_queue, unhandled_responses_sync_dict
from grld_server import GrldServer, GrldServerException
from grld_channels import GrldChannels

class NetworkException(BaseException):
    pass

class GrldPushCommandNames:
    BREAK = 'break'
    SYNCHRONIZE = 'synchronize'

def is_break_command(message):
    message == GrldPushCommandNames.BREAK

def is_synchronize_command(message):
    message == GrldPushCommandNames.SYNCHRONIZE


KEEP_ALIVE_INTERVAL = 1 # seconds

class GrldBreakPushCommand:
    def __init__(self, filename, lineno):
        self.filename = filename
        self.lineno = lineno

class NetWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.grld_server = GrldServer()
        self.last_keep_alive_time = 0

        self.__stop = False

        return super().__init__(*args, **kwargs)


    def send_keep_alive(self):
        t = time.clock()
        if (t - self.last_check_time) >= KEEP_ALIVE_INTERVAL: # need to rate-limit this so we don't flood the network
            self.last_keep_alive_time = t
            self.send('', GrldChannels.KEEP_ALIVE)

    def stop(self):
        self.__stop = True

    def run(self):
        while not self.__stop:
            if not self.grld_server.is_connected():
                try:
                    self.grld_server.listen()
                except GrldServerException as e:
                    # TODO: what do we do if we hit an error connecting to the GRLD client?
                    raise


            self.send_keep_alive()

            transaction = net_request_transaction_queue.get_nowait()
            if not transaction:
                continue

            for request in transaction.requests:
                try:
                    self.grld_server.send(request.data, request.channel)
                except:
                    raise # TODO: What do we do if we fail to send data to the GRLD client?


            messages = self.grld_server.read()
            while not messages and transaction.expects_response:
                time.sleep(0.1)
                messages = self.grld_server.read()
                # TODO: timeout?


            i = 0
            response_messages = []
            while i < len(messages):
                message = messages[i]

                if is_break_command(message):
                    break_push_command = GrldBreakPushCommand(messages[i+1], messages[i+2])
                    unhandled_grld_push_command_queue.put(break_push_command)
                    i += 2

                elif is_synchronize_command(message):
                    # handling this here because we need to respond immediately

                    # synchronize expects us to return the # of active breakpoints (this is actually not implemented, we MUST return 0 here)
                    self.grld_server.send(0, GrldChannels.PAUSED)

                    # next we need to send the "breakOnConnection" value, this is configurable, but we'll just always return false for now
                    self.grld_server.send(False, GrldChannels.PAUSED)

                else:
                    response_messages.append(message)

                i += 1

            unhandled_responses_sync_dict.set(transaction.id, response_messages)
