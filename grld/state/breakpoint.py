class Breakpoint(dict):
    __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    __eq__(self, other):
        return self['local_path'] == other['local_path'] and self['confirmed'] == other['confirmed']

def create_breakpoint(local_path, lineno, confirmed=False):
    return Breakpoint({
        'local_path': local_path
        'lineno': lineno
        'confirmed': confirmed
    })