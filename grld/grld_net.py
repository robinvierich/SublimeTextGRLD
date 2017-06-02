from id_generator import IdGenerator

from grld_command_helpers import GrldCommandNames

from shared_queues import net_request_queue, net_response_queue, request_transaction_queue

# grld expects to receive commands on one of these channels based on its current execution state
class Channels:
    PAUSED ='default',  # lua is NOT running (i.e. execution is broken)
    RUNNING = 'running' # lua is running
    KEEP_ALIVE = 'ka'   # used to ensure socket connection is still ok and prevent timeouts


def block_for_response(request_transaction_id):
    while True:
        response = unhandled_responses.get(request_transaction_id)
        if response: break
        time.sleep(0.1)

    return response


def error_if_sent(func):
    def wrapper(self, *args, **kwargs):
        assert (not self.sent), "This request transaction was already sent!"
        return func(self, *args, **kwargs)

    return wrapper


class RequestTransaction:
    id_generator = IdGenerator(lambda x: "req_trans{}".format(x))

    @classmethod
    def send_single_request(cls, request_data, channel = None):
        transaction = cls()

        if channel:
            transaction.add_request(request_data, channel)
        else:
            transaction.add_request(request_data)

        transaction.commit()


    def __init__(self):
        self.id = RequestTransaction.id_generator.get_next_id()
        self.requests = []
        self.expects_response = False
        self.sent = False

    @error_if_sent
    def add_request(self, request_data, channel = Channels.PAUSED):
        """
        Queues a request to be sent.

        request_data: a string or a dictionary
        """

        request = Request(request_data, channel)
        self.requests.append(request)

    @error_if_sent
    def send(self):
        self.sent = True
        request_transaction_queue.append(self)
        return self.id

    @error_if_sent
    def send_and_block_for_response(self):
        self.send()
        self.expects_response = True

        return block_for_response(self.id)



class Request:
    id_generator = IdGenerator(lambda x: "req{}".format(x))

    def __init__(self, data, channel):
        self.id = Request.id_generator.get_next_id()
        self.data = data
        self.channel = channel


class Response:
    def __init__(self, response_data, request):
        self.response_data = response_data
        self.request_id = request.id
