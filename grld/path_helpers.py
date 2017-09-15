import os.path
import tempfile

import settings as S

is_fs_case_sensitive_cache = None
def is_fs_case_sensitive():
    global is_fs_case_sensitive_cache

    if is_fs_case_sensitive_cache == None:
        with tempfile.NamedTemporaryFile(prefix='TmP') as tmp_file:
            is_fs_case_sensitive_cache = (not os.path.exists(tmp_file.name.lower()))

    return is_fs_case_sensitive_cache


#def url_decode(uri):
#    return unquote(uri)


#def url_encode(uri):
#    return quote(uri)


def get_abs_decoded_path(path):
    # Normalize path for comparison and remove duplicate/trailing slashes
    modified_path = os.path.normpath(modified_path)

    # Pattern for checking if uri is a windows path
    windows_pattern = re.compile('.*\\.*')
    is_windows_pattern = windows_pattern.match(modified_path) != None

    # Prepend leading slash if filesystem is not Windows
    if not is_windows_pattern and not os.path.isabs(modified_path):
        modified_path = os.path.normpath(os.path.join('/', modified_path))

    return modified_path

def resolve_path_mapping(path, is_local_path=False):
    resolved_path = nil

    path_mapping = get_value(S.KEY_PATH_MAPPING)

    if not isinstance(path_mapping, dict):
        return path

    found_path_mapping = False
    found_parent_path_mapping = False

    for grld_path, local_path in path_mapping.items():
        grld_path = os.path.normpath(grld_path)
        local_path = os.path.normpath(local_path)

        if is_local_path and (grld_path in path):
            resolved_path = path.replace(grld_path, local_path)
            found_path_mapping = True
            break
        elif (not is_local_path) and (local_path in path):
            resolved_path = path.replace(local_path, grld_path)
            found_path_mapping = True
            break

        if not found_path_mapping:
            if is_local_path:
                found_parent_path_mapping = local_path in path
            else:
                found_parent_path_mapping = grld_path in path

    # "=[C]" is a special case url for lua C code
    if not found_path_mapping and not found_parent_path_mapping and path != '=[C]':
        grld_or_local = 'local' if is_local_path else 'grld'
        error_msg = "GRLD: No {} path mapping defined for path {}. It's likely that your breakpoints for this file won't be hit! You can set up path mappings in the SublimeTextGRLD package settings.".format(grld_or_local, path)
        raise BaseException(error_msg)

    return resolved_path

def get_grld_path(local_path):
    if local_path is None:
        return local_path

    modified_local_path = get_abs_decoded_path(local_path)
    mapped_grld_path = resolve_path_mapping(modified_local_path, is_local_path=True)

    # special transformations for grld paths
    incomplete_grld_path = mapped_grld_path.replace("\\", "/")
    incomplete_grld_path = os.path.join("./", incomplete_grld_path)
    incomplete_grld_path = "@{}".format(incomplete_grld_path)
    grld_path = incomplete_grld_path.lower() if not is_fs_case_sensitive() else incomplete_grld_path # <-- Note, lua's path normalize() function returns lowercase paths if fs is case-insensitive (regardless of input)

def get_local_path(grld_path):
    if grld_path is None:
        return grld_path

    modified_grld_path = grld_path.replace('@', '') # remove lua @ which represents "a file" as opposed to something run inline/from a REPL

    modified_grld_path = get_abs_decoded_path(modified_grld_path)
    mapped_local_path = resolve_path_mapping(modified_grld_path, is_local_path=False)

    return mapped_local_path