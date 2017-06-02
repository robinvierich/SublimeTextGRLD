class GrldCommandNames:
    SET_BREAKPOINT = 'setbreakpoint'

    GET_LOCALS = 'locals'
    GET_UPVALUES = 'upvalues'
    GET_STACK = 'stack'
    GET_COROUTINES = 'coroutines'

    EVALUATE = 'evaluate'

    STEP_OVER = 'stepover'
    STEP_IN = 'stepin'
    STEP_OUT = 'stepout'
    PAUSE = 'break'
    RESUME = 'run'


def create_breakpoint_request_data(source_filename, lineno, active):
    return {"source": source_filename, "line": int(lineno), "value": active}