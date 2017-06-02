from collections import OrderedDict

from grld_net import send_request, block_for_response, Channels, RequestTransaction
from grld_command_helpers import GrldCommandNames, create_breakpoint_request_data

def set_breakpoint(local_path, lineno, active):
    """
    Add or remove a breakpoint from specified file and line number.
    """

    if not filename or not lineno:
        return

    grld_path = get_grld_path(local_path)
    breakpoint_request_data = create_breakpoint_request_data(grld_path, lineno, active)
    
    transaction = RequestTransaction()
    transaction.add_request(GrldCommandNames.SET_BREAKPOINT, Channels.RUNNING)
    transaction.add_request(breakpoint_request_data, Channels.RUNNING)


def add_breakpoint(local_path, lineno):
    """
    Add a breakpoint from specified file and line number.
    """

    set_breakpoint(local_path, lineno, True)


def remove_breakpoint(local_path, lineno):
    """
    Remove a breakpoint from specified file and line number.
    """

    set_breakpoint(local_path, lineno, False)


def evaluate_expression(expression, thread, stack_level):
    transaction = RequestTransaction()
    transaction.add_request(GrldCommandNames.EVALUATE)
    transaction.add_request('=' + expression) #TODO: should we always add '='?
    transaction.add_request(thread)
    transaction.add_request(stack_level)
    response = transaction.send_and_block_for_response()

    return response


def get_upvalues(thread, stack_level):
    """
    Get upvalues in given thread and stack_level.
    """

    transaction = RequestTransaction()
    transaction.add_request(GrldCommandNames.GET_LOCALS)
    transaction.add_request(thread)
    transaction.add_request(stack_level)
    response = transaction.send_and_block_for_response()

    return response


def get_locals(thread, stack_level):
    """
    Get locals in given thread and stack_level.
    """

    transaction = RequestTransaction()
    transaction.add_request(GrldCommandNames.GET_LOCALS)
    transaction.add_request(thread)
    transaction.add_request(stack_level)
    response = transaction.send_and_block_for_response()

    return response


def get_stack(thread):
    """
    Get stack information for current context.
    """

    transaction = RequestTransaction()
    transaction.add_request(GrldCommandNames.GET_STACK)
    transaction.add_request(thread)
    response = transaction.send_and_block_for_response()

    return response


def get_coroutines():
    transaction = RequestTransaction()
    transaction.add_request(GrldCommandNames.GET_COROUTINES)
    response = transaction.send_and_block_for_response()

    # always include a 'main' coroutine. This is how GRLD references the main Lua thread (but it's not returned explicitly from a 'coroutines' query)
    count = len(response.keys()) 
    response[count + 1] = {'id': 'main'}

    return response


def step_in():
    RequestTransaction.send_single_request(GrldCommandNames.STEP_IN)


def step_over():
    RequestTransaction.send_single_request(GrldCommandNames.STEP_OVER)


def step_out():
    RequestTransaction.send_single_request(GrldCommandNames.STEP_OUT)


def resume():
    RequestTransaction.send_single_request(GrldCommandNames.RESUME)


def pause():
    RequestTransaction.send_single_request(GrldCommandNames.PAUSE)





# TODO: This is just a list of expressions.. we should handle this higher up as it isn't a separate command

#def get_watch_values(watch_expressions, thread, stack_level):
#    """
#    Evaluate watch expressions in specified context.

#    watch_expressions: list of expressions to evaluate

#    returns list of evaluated responses in order
#    """

#    watch_expression_values = []

#    for watch_expression in watch_expressions:
#        value = evaluate_expression(watch_expression, thread, stack_level)
#        watch_expression_values.append(value)

#    return watch_expression_values


