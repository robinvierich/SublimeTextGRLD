def create_lua_stack_frame(local_source_file_path, lineno, what, name, namewhat, stack_level):
    return {
        'local_source_file_path': local_source_file_path
        'lineno': lineno
        'what': what
        'name': name
        'namewhat': namewhat
        'stack_level': stack_level
    }

