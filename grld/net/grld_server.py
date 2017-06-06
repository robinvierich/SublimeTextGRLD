import socket
import select

from grld_protocol_helpers import *

class ConnectionState:
    DISCONNECTED = 0
    LISTENING = 1
    CONNECTED = 2

GRLD_PORT = 4242
SOCKET_READ_BYTES_COUNT = 1024
MAX_READ_FAILURE_COUNT = 5

class GrldServerException(BaseException):
    pass


def encode(str):
    return str.encode('utf8')


def decode(str):
    return str.decode('utf8')


def assert_connected(func):
    def wrapper(self, *args, **kwargs):
        assert self.connection_state == ConnectionState.CONNECTED, "The GRLD server is not connected to a client!"
        return func(self, *args, **kwargs)

    return wrapper

class GrldServer:
    def __init__(self, port = GRLD_PORT):
        self.socket = None
        self.socket_read_bytes_count = SOCKET_READ_BYTES_COUNT

        self.port = port
        self.connection_state = ConnectionState.DISCONNECTED

        self.read_buffer = ''
        self.read_failure_count = 0

    def is_connected(self):
        return self.connection_state == ConnectionState.CONNECTED

    @assert_connected
    def disconnect(self):
        pass

    def _does_socket_have_data_ready(self):
        ready_read_descriptors, _, _ = select.select([self.socket], [], [], 0)
        return bool(ready_read_descriptors)
            

    @assert_connected
    def _read_from_socket(self):
        buffer = ''

        try:
            while self._does_socket_have_data_ready():
                encoded_socket_data = self.socket.recv(self.socket_read_bytes_count)
                if not encoded_socket_data:
                    break

                buffer += decode(encoded_socket_data)

        except:
            e = sys.exc_info()[1]
            raise GrldServerException(e)
        
        return buffer

    def parse_messages_from_read_buffer(self):
        if not self.read_buffer:
            return []

        while True:
            lines = self.read_buffer.split("\n")

            if len(lines) % 3 != 0:
                # probably don't have all the data yet, or there was a comm error.
                self.read_failure_count += 1
                return

            # message: (channel, data_len, data)
            messages = ((lines[i-2], lines[i-1], lines[i]) for i in range(2, len(lines), 3))
            deserialized_messages = (deserialize(message[2]) for message in messages)

        return messages


    @assert_connected
    def read(self):
        read_data = self._read_from_socket()
        if not read_data:
            return ''

        self.read_buffer += read_data

        messages = self.parse_messages_from_read_buffer()

        if self.read_failure_count > MAX_READ_FAILURE_COUNT:
            raise GrldServerException("Error reading/parsing data from GRLD")

        return messages


    @assert_connected
    def send(self, data, channel):
        serialized_data = serialize_data(data)
        message = serialize_to_message(serialized_data, channel)

        exception = None
        try:
            encoded_message = encode(message)
            sent = self.socket.send(encoded_message)
        except socket.error as e:
            sent = 0
            exception = e

        if sent == 0:
            raise GrldServerException(exception)


    def listen():
        """
        Create socket server which listens for connection on configured port.
        """
        assert self.connection_state == ConnectionState.DISCONNECTED, "Cannot start listening unless currently disconnected"

        # Create socket server
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not listen_socket:
            raise ProtocolConnectionException('Could not create socket to listen for GRLD connections.')

        # Configure socket server
        try:
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listen_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            listen_socket.settimeout(1)
            listen_socket.bind(('', self.port))
            listen_socket.listen(1)

            self.connection_state = ConnectionState.LISTENING
        except:
            e = sys.exc_info()[1]
            raise GrldServerException(e)

        # Accept incoming connection on configured port
        while not self.listening_canceled_event.is_set() and self.listening:
            try:
                self.socket, address = listen_socket.accept()
                self.listening = False
            except socket.timeout:
                raise GrldServerException("socket timeout")
            except BaseException as e:
                raise GrldServerException(e)

        # Check if a connection has been made
        if self.socket:
            self.connection_state = ConnectionState.CONNECTED
            self.socket.settimeout(None)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        else:
            self.connection_state = ConnectionState.DISCONNECTED
            raise GrldServerException("error accepting connection")

        try:
            listen_socket.close()
        except BaseException as e:
            raise GrldServerException(e)
