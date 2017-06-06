import time

from grld.id_generator import IdGenerator
from grld.shared_data import unhandled_responses

from grld_command_names import GrldCommandNames


def error_if_sent(func):
    def wrapper(self, *args, **kwargs):
        assert (not self.sent), "This request transaction was already sent!"
        return func(self, *args, **kwargs)

    return wrapper


class Request:
    id_generator = IdGenerator(lambda x: "req{}".format(x))

    def __init__(self, data, channel):
        self.id = Request.id_generator.get_next_id()
        self.data = data
        self.channel = channel


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
    def add_request(self, request_data, channel = GrldChannels.PAUSED):
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

        return self.block_for_response()


    def block_for_response(self):
        while True:
            response = unhandled_responses.get(self.id)
            if response: break
            time.sleep(0.1)

        return response

