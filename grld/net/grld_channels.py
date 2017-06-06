# grld expects to receive commands on one of these channels based on its current execution state
class GrldChannels:
    PAUSED ='default',  # lua is NOT running (i.e. execution is broken)
    RUNNING = 'running' # lua is running
    KEEP_ALIVE = 'ka'   # used to ensure socket connection is still ok and prevent timeouts