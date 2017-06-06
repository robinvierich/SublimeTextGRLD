import sublime
import sublime_plugin

from debugger_state import DebuggerState
from shared_data import command_queue

from grld.commands.add_breakpoint import AddBreakpointCommand


def get_local_path_for_breakpoint(view):
    # Get filename in current view and check if is a valid filename
    if filename is None:
        filename = view.file_name()
    if not filename or not os.path.isfile(filename):
        return None

    return filename


def get_lineno_for_breakpoint(view):
    # Add entry for file in breakpoint data
    if filename not in S.BREAKPOINT:
        S.BREAKPOINT[filename] = {}

    # When no rows are defined, use selected rows (line numbers), filtering empty rows
    if rows is None:
        rows = V.region_to_rows(self.view.sel(), filter_empty=True)

    # return the last row if multiple are selected
    if rows:
        return rows[-1]


class GrldBreakpointCommand(sublime_plugin.TextCommand):
    """
    Add/Remove breakpoint(s) for rows (line numbers) in selection.
    """
    def run(self, edit, rows=None, condition=None, enabled=None, filename=None):
        local_path = get_local_path_for_breakpoint(self.view)
        lineno = get_lineno_for_breakpoint(self.view)

        breakpoint_exists = ui_debugger_state.does_breakpoint_exist(local_path, lineno)

        if breakpoint_exists:
            remove_breakpoint_command = RemoveBreakpointCommand()
            command_queue.put(remove_breakpoint_command)
        else:
            add_breakpoint_command = AddBreakpointCommand()
            command_queue.put(add_breakpoint_command)



        # Save breakpoint data to file
        # util.save_breakpoint_data()

#class GrldRenderIconsCommand(sublime_plugin.TextCommand):
#    def run(self, edit, code_view_id=None):
#        if not code_view_id:
#            return

#        code_view = None
#        for view in self.view.window().views():
#            if view.id() == code_view_id:
#                code_view = view
#                break
        
#        if not code_view:
#            return

#        num_code_lines = len(code_view.lines(sublime.Region(0, code_view.size())))
        
#        newlines_str = ' \n' * (num_code_lines - 1)

#        self.view.set_read_only(False)
#        num_icon_lines = len(self.view.lines(sublime.Region(0, self.view.size())))
#        if num_icon_lines != num_code_lines - 1:
#            self.view.erase(edit, sublime.Region(0, self.view.size()))
#            self.view.insert(edit, 0, newlines_str)
#        else:
#            self.view.replace(edit, sublime.Region(0, self.view.size()), newlines_str)
#        self.view.set_read_only(True)

#        pos = code_view.viewport_position()
#        sublime.set_timeout(lambda: self.view.set_viewport_position(pos, False), 0)
#        sublime.set_timeout(lambda: V._render_regions(code_view, self.view), 0)

#class GrldConditionalBreakpointCommand(sublime_plugin.TextCommand):
#    """
#    Add conditional breakpoint(s) for rows (line numbers) in selection.
#    """
#    def run(self, edit):
#        self.view.window().show_input_panel('Breakpoint condition', '', self.on_done, self.on_change, self.on_cancel)

#    def on_done(self, condition):
#        self.view.run_command('grld_breakpoint', {'condition': condition, 'enabled': True})

#    def on_change(self, line):
#        pass

#    def on_cancel(self):
#        pass


class GrldClearBreakpointsCommand(sublime_plugin.TextCommand):
    """
    Clear breakpoints in selected view.
    """
    def run(self, edit):



        filename = self.view.file_name()
        if filename and filename in S.BREAKPOINT:
            rows = H.dictionary_keys(S.BREAKPOINT[filename])
            self.view.run_command('grld_breakpoint', {'rows': rows, 'filename': filename})

    def is_enabled(self):
        filename = self.view.file_name()
        if filename and S.BREAKPOINT and filename in S.BREAKPOINT and S.BREAKPOINT[filename]:
            return True
        return False

    def is_visible(self):
        filename = self.view.file_name()
        if filename and S.BREAKPOINT and filename in S.BREAKPOINT and S.BREAKPOINT[filename]:
            return True
        return False


class GrldClearAllBreakpointsCommand(sublime_plugin.WindowCommand):
    """
    Clear breakpoints from all views.
    """
    def run(self):
        view = sublime.active_window().active_view()
        # Unable to run to line when no view available
        if view is None:
            return

        for filename, breakpoint_data in S.BREAKPOINT.items():
            if breakpoint_data:
                rows = H.dictionary_keys(breakpoint_data)
                view.run_command('grld_breakpoint', {'rows': rows, 'filename': filename})

    def is_enabled(self):
        if S.BREAKPOINT:
            for filename, breakpoint_data in S.BREAKPOINT.items():
                if breakpoint_data:
                    return True
        return False

    def is_visible(self):
        if S.BREAKPOINT:
            for filename, breakpoint_data in S.BREAKPOINT.items():
                if breakpoint_data:
                    return True
        return False


class GrldSessionStartCommand(sublime_plugin.WindowCommand):
    """
    Start GRLD session, listen for request response from debugger engine.
    """
    def run(self, restart=False):
        S.PROTOCOL = protocol.Protocol(lambda e: self.on_connection_lost(e))
        S.SESSION_BUSY = False
        S.BREAKPOINT_EXCEPTION = None
        S.BREAKPOINT_ROW = None
        S.CONTEXT_DATA.clear()
        async_session = session.SocketHandler(session.ACTION_WATCH, check_watch_view=True)
        async_session.start()
        # Remove temporary breakpoint
        if S.BREAKPOINT_RUN is not None and S.BREAKPOINT_RUN['filename'] in S.BREAKPOINT and S.BREAKPOINT_RUN['lineno'] in S.BREAKPOINT[S.BREAKPOINT_RUN['filename']]:
            self.window.active_view().run_command('grld_breakpoint', {'rows': [S.BREAKPOINT_RUN['lineno']], 'filename': S.BREAKPOINT_RUN['filename']})
        S.BREAKPOINT_RUN = None
        # Set debug layout

        sublime.set_timeout(lambda: self.window.run_command('grld_layout'), 0)

        # Start thread which will run method that listens for response on configured port
        threading.Thread(target=self.listen).start()
        sublime.set_timeout(refresh_views_loop, 0)

    # note: may be called from a separate thread (not main thread)
    def on_connection_lost(self, exception):
        sublime.set_timeout(lambda: self.window.run_command('grld_session_restart'), 0)
        sublime.set_timeout(lambda: sublime.status_message('The connection to client was lost. SublimeTextGRLD server was restarted and is waiting for connections..'), 0)

    def listen(self):
        # Start listening for response from debugger engine
        with S.PROTOCOL as protocol:
            S.PROTOCOL.listen()

        # On connect run method which handles connection
        if S.PROTOCOL and S.PROTOCOL.connected:
            self.connected()

    def connected(self):
        sublime.set_timeout(lambda: sublime.status_message('GRLD: Connected'), 100)

        async_session = session.SocketHandler(session.ACTION_INIT)
        async_session.start()

    def is_enabled(self):
        if S.PROTOCOL:
            return False
        return True

    def is_visible(self):
        if S.PROTOCOL:
            return False
        return True


class GrldSessionRestartCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('grld_session_stop', {'restart': True})
        self.window.run_command('grld_session_start', {'restart': True})

    def is_enabled(self):
        if S.PROTOCOL:
            return True
        return False

    def is_visible(self):
        if S.PROTOCOL:
            return True
        return False


class GrldSessionStopCommand(sublime_plugin.WindowCommand):
    """
    Stop GRLD session, close connection and stop listening to debugger engine.
    """
    def run(self, close_windows=False, restart=False):
        try:
            S.PROTOCOL.stop_listening_for_incoming_connections()
            with S.PROTOCOL as protocol:
                protocol.clear()
        except BaseException as e:
            print(e)
            pass

        finally:
            S.PROTOCOL = None
            S.SESSION_BUSY = False
            S.BREAKPOINT_EXCEPTION = None
            S.BREAKPOINT_ROW = None
            S.CONTEXT_DATA.clear()
            async_session = session.SocketHandler(session.ACTION_WATCH, check_watch_view=True)
            async_session.start()
            # Remove temporary breakpoint
            if S.BREAKPOINT_RUN is not None and S.BREAKPOINT_RUN['filename'] in S.BREAKPOINT and S.BREAKPOINT_RUN['lineno'] in S.BREAKPOINT[S.BREAKPOINT_RUN['filename']]:
                self.window.active_view().run_command('grld_breakpoint', {'rows': [S.BREAKPOINT_RUN['lineno']], 'filename': S.BREAKPOINT_RUN['filename']})
            S.BREAKPOINT_RUN = None
        # Close or reset debug layout
        if close_windows or config.get_value(S.KEY_CLOSE_ON_STOP):
            if config.get_value(S.KEY_DISABLE_LAYOUT):
                sublime.set_timeout(lambda: self.window.run_command('grld_layout', {'close_windows': True}), 0)
            else:
                sublime.set_timeout(lambda: self.window.run_command('grld_layout', {'restore': True}), 0)
        else:
            sublime.set_timeout(lambda: self.window.run_command('grld_layout'), 0)

    def is_enabled(self):
        if S.PROTOCOL:
            return True
        return False

    def is_visible(self, close_windows=False):
        if S.PROTOCOL:
            if close_windows and config.get_value(S.KEY_CLOSE_ON_STOP):
                return False
            return True
        return False

class GrldBreakCommand(sublime_plugin.WindowCommand):
    """
    Break execution immediately.
    """
    def run(self):
        async_session = session.SocketHandler(session.ACTION_BREAK)
        async_session.start()

    def is_enabled(self):
        return session.is_connected()

class GrldExecuteCommand(sublime_plugin.WindowCommand):
    """
    Execute command, handle breakpoints and reload session when page execution has completed.

    Keyword arguments:
    command -- Command to send to debugger engine.
    """
    def run(self, command=None):
        async_session = session.SocketHandler(session.ACTION_EXECUTE, command=command)
        async_session.start()

    def is_enabled(self):
        return session.is_connected()


class GrldContinueCommand(sublime_plugin.WindowCommand):
    """
    Continuation commands when on breakpoint, show menu by default if no command has been passed as argument.

    Keyword arguments:
    command -- Continuation command to execute.
    """
    commands = H.new_dictionary()
    commands[grld.RUN] = 'Run'
    commands[grld.STEP_OVER] = 'Step Over'
    commands[grld.STEP_IN] = 'Step In'
    commands[grld.STEP_OUT] = 'Step Out'
    commands[grld.BREAK] = 'Break'

    command_index = H.dictionary_keys(commands)
    command_options = H.dictionary_values(commands)

    def run(self, command=None):
        if not command or not command in self.commands:
            self.window.show_quick_panel(self.command_options, self.callback)
        else:
            self.callback(command)

    def callback(self, command):
        if command == -1 or S.SESSION_BUSY:
            return
        if isinstance(command, int):
            command = self.command_index[command]

        self.window.run_command('grld_execute', {'command': command})

    def is_enabled(self):
        return S.BREAKPOINT_ROW is not None and session.is_connected()

    def is_visible(self):
        return S.BREAKPOINT_ROW is not None and session.is_connected()


class GrldStatusCommand(sublime_plugin.WindowCommand):
    """
    Get status from debugger engine.
    """
    def run(self):
        async_session = session.SocketHandler(session.ACTION_STATUS)
        async_session.start()

    def is_enabled(self):
        return session.is_connected()

    def is_visible(self):
        return session.is_connected()

class GrldUpdateEvaluateLineResponseCommand(sublime_plugin.TextCommand):
    def run(self, edit, response):
        end_of_view_point = self.view.size()

        last_char = self.view.substr(sublime.Region(end_of_view_point - 1, end_of_view_point))
        if last_char != '\n':
            format_string  = "\n==> {}\n"
        else:
            format_string  = "==> {}\n"

        self.view.insert(edit, self.view.size(), format_string.format(response))

class GrldEvaluateLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        #self.window.show_input_panel('Evaluate', '', self.on_done, self.on_change, self.on_cancel)
        sel = self.view.sel()
        if len(sel) > 1:
            self.view.show_popup('cannot evaluate: selection is invalid')

        region = sel[0]
        line_region = self.view.line(region)
        line_contents = self.view.substr(line_region)

        async_session = session.SocketHandler(session.ACTION_EVALUATE, expression=line_contents, view=self.view)
        async_session.start()

    def is_enabled(self):
        return session.is_connected()

    def is_visible(self):
        return session.is_connected()

class GrldSetCurrentStackLevelCommand(sublime_plugin.WindowCommand):
    """
    Set the current stack level that's being inspected. Important for variable evaluation.
    """

    def run(self, stack_level):
        async_session = session.SocketHandler(session.ACTION_SET_CURRENT_STACK_LEVEL, stack_level=stack_level)
        async_session.start()

class GrldSetSelectedThread(sublime_plugin.WindowCommand):
    """
    Select a thread we want to inspect.
    """

    def run(self, selected_thread):
        async_session = session.SocketHandler(session.ACTION_SET_SELECTED_THREAD, selected_thread=selected_thread)
        async_session.start()

class GrldUserExecuteCommand(sublime_plugin.WindowCommand):
    """
    Open input panel, allowing user to execute arbitrary command according to DBGp protocol.
    Note: Transaction ID is automatically generated by session module.
    """
    def run(self):
        self.window.show_input_panel('DBGp command', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, line):
        # Split command and arguments, define arguments when only command is defined.
        if ' ' in line:
            command, args = line.split(' ', 1)
        else:
            command, args = line, ''

        async_session = session.SocketHandler(session.ACTION_USER_EXECUTE, command=command, args=args)
        async_session.start()

    def on_change(self, line):
        pass

    def on_cancel(self):
        pass

    def is_enabled(self):
        return session.is_connected()

    def is_visible(self):
        return session.is_connected()


class GrldWatchCommand(sublime_plugin.WindowCommand):
    """
    Add/Edit/Remove watch expression.
    """
    def run(self, clear=False, edit=False, remove=False, update=False):
        self.edit = edit
        self.remove = remove
        self.watch_index = None
        # Clear watch expressions in list
        if clear:
            try:
                # Python 3.3+
                S.WATCH.clear()
            except AttributeError:
                del S.WATCH[:]
            # Update watch view
            self.update_view()
        # Edit or remove watch expression
        elif edit or remove:
            # Generate list with available watch expressions
            watch_options = []
            for index, item in enumerate(S.WATCH):
                watch_item = '[{status}] - {expression}'.format(index=index, expression=item['expression'], status='enabled' if item['enabled'] else 'disabled')
                watch_options.append(watch_item)
            self.window.show_quick_panel(watch_options, self.callback)
        elif update:
            self.update_view()
        # Set watch expression
        else:
            self.set_expression()

    def callback(self, index):
        # User has cancelled action
        if index == -1:
            return
        # Make sure index is valid integer
        if isinstance(index, int) or H.is_digit(index):
            self.watch_index = int(index)
            # Edit watch expression
            if self.edit:
                self.set_expression()
            # Remove watch expression
            else:
                S.WATCH.pop(self.watch_index)
                # Update watch view
                self.update_view()

    def on_done(self, expression):
        # User did not set expression
        if not expression:
            return
        # Check if expression is not already defined
        matches = [x for x in S.WATCH if x['expression'] == expression]
        if matches:
            sublime.status_message('GRLD: Watch expression already defined.')
            return
        # Add/Edit watch expression in session
        watch = {'expression': expression, 'enabled': True, 'value': None, 'type': None}
        if self.watch_index is not None and isinstance(self.watch_index, int):
            try:
                S.WATCH[self.watch_index]['expression'] = expression
            except:
                S.WATCH.insert(self.watch_index, watch)
        else:
            S.WATCH.append(watch)
        # Update watch view
        self.update_view()

    def on_change(self, line):
        pass

    def on_cancel(self):
        pass

    def set_expression(self):
        # Show user input for setting watch expression
        self.window.show_input_panel('Watch expression', '', self.on_done, self.on_change, self.on_cancel)

    def update_view(self):
        async_session = session.SocketHandler(session.ACTION_WATCH, check_watch_view=True)
        async_session.start()
        # Save watch data to file
        util.save_watch_data()

    def is_visible(self, clear=False, edit=False, remove=False):
        if (clear or edit or remove) and not S.WATCH:
            return False
        return True


class GrldViewUpdateCommand(sublime_plugin.TextCommand):
    """
    Update content of sublime.Edit object in view, instead of using begin_edit/end_edit.

    Keyword arguments:
    data -- Content data to populate sublime.Edit object with.
    readonly -- Make sublime.Edit object read only.
    """
    def run(self, edit, data=None, readonly=False):
        view = self.view
        view.set_read_only(False)
        view.erase(edit, sublime.Region(0, view.size()))
        if data is not None:
            view.insert(edit, 0, data)
        if readonly:
            view.set_read_only(True)


class GrldLayoutCommand(sublime_plugin.WindowCommand):
    """
    Toggle between debug and default window layouts.
    """
    def run(self, restore=False, close_windows=False, keymap=False):
        # Get active window
        window = self.window
        # Do not restore layout or close windows while debugging
        if S.PROTOCOL and (restore or close_windows or keymap):
            return
        # Set layout, unless user disabled debug layout
        if not config.get_value(S.KEY_DISABLE_LAYOUT):
            if restore or keymap:
                V.set_layout('normal')
            else:
                V.set_layout('debug')
        # Close all debugging related windows
        if close_windows or restore or keymap:
            V.close_debug_windows()
            return

        sublime.set_timeout(lambda: self.clear_content(), 100)
        
        panel = window.get_output_panel('grld')
        panel.run_command("grld_view_update")
        # Close output panel
        window.run_command('hide_panel', {"panel": 'output.grld'})

        #self.clear_content()

    def clear_content(self):
        window = self.window

        # Reset data in debugging related windows
        V.show_content(V.DATA_BREAKPOINT)
        V.show_content(V.DATA_CONTEXT)
        V.show_content(V.DATA_STACK)
        V.show_content(V.DATA_WATCH)
        V.show_content(V.DATA_COROUTINES)

        # don't override content of evaluate window automatically
        evaluate_content = ''
        icons_content = ''
        for v in window.views():
            if v.name() == V.TITLE_WINDOW_EVALUATE:
                evaluate_content = v.substr(sublime.Region(0, v.size()))
            if v.name() == V.TITLE_WINDOW_ICONS:
                icons_content = v.substr(sublime.Region(0, v.size()))

        V.show_content(V.DATA_EVALUATE, evaluate_content)
        V.show_content(V.DATA_ICONS, icons_content)

    def is_enabled(self, restore=False, close_windows=False):
        disable_layout = config.get_value(S.KEY_DISABLE_LAYOUT)
        if close_windows and (not disable_layout or not V.has_debug_view()):
            return False
        if restore and disable_layout:
            return False
        return True

    def is_visible(self, restore=False, close_windows=False):
        if S.PROTOCOL:
            return False
        disable_layout = config.get_value(S.KEY_DISABLE_LAYOUT)
        if close_windows and (not disable_layout or not V.has_debug_view()):
            return False
        if restore and disable_layout:
            return False
        if restore:
            try:
                return sublime.active_window().get_layout() == config.get_value(S.KEY_DEBUG_LAYOUT, S.LAYOUT_DEBUG)
            except:
                pass
        return True


class GrldSettingsCommand(sublime_plugin.WindowCommand):
    """
    Show settings file.
    """
    def run(self, default=True):
        # Show default settings in package when available
        if default and S.PACKAGE_FOLDER is not None:
            package = S.PACKAGE_FOLDER
        # Otherwise show User defined settings
        else:
            package = "User"
        # Strip .sublime-package of package name for syntax file
        package_extension = ".sublime-package"
        if package.endswith(package_extension):
            package = package[:-len(package_extension)]
        # Open settings file
        self.window.run_command('open_file', {'file': '${packages}/' + package + '/' + S.FILE_PACKAGE_SETTINGS });


