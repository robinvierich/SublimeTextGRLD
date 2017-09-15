

class BaseView:
    def __init__(self, name, layout_data, window):

        open_view = None

        for view in window.views():
            if name == view.name():
                open_view = view
                break

        if not open_view:
            view = window.new_file()
            view.set_scratch(True)
            view.set_read_only(True)
            view.set_name(title)
            window.set_view_index(view, layout_data['group'], layout_data['index'])

class EvaluateView(BaseView):
    def __init__(self, layout_data, window):

        self.name = 'evaluate'

        self.layout_index = debug_layout_view_data['evaluate'].index
        self.layout_group = debug_layout_view_data.group

        self.sublime_view = sublime_view

        super().__init__(self, 'evaluate', layout_data)

    # on click

    def __get_breakpoint_line(self, breakpoint):
        return str.format('[{stack_level}] {filename}:{lineno} - {name}({namewhat})', breakpoint)

    def get_contents(self, debugger_state):
        content_lines = (self.__get_breakpoint_line(breakpoint) for breakpoint in debugger_state['breakpoints'])

        return "\n".join(content_lines)