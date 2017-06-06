from grld.net.net_worker import NetWorker
from grld.command_worker import CommandWorker


def main():
    net_worker = NetWorker()
    net_worker.start()

    command_worker = CommandWorker()
    command_worker.start()