from debugger_state import add_evaluated_expression_response

from grld.net_commands import evaluate_expression

class EvaluateExpressionCommand:
    def __init__(self, expression):
        self.expression = expression

    def execute(self, debugger_state):
        thread = debugger_state['lua_execution_state']['current_thread']
        stack_level = debugger_state['lua_execution_state']['current_stack_level']
        expression = self.expression

        response = evaluate_expression(expression, thread, stack_level)

        add_evaluated_expression_response(debugger_state, expression, thread, stack_level, response)

        return debugger_state