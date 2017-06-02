import re

def serialize_data( value ):
    t = type( value )
    if t == int or t == float:
        if value == float('inf'):
            res = infStr
        elif value == -float('inf'):
            res = negInfStr
        elif value == float('nan'):
            res = nanStr
        else:
            res = str( value )

        return res
    elif t == bool:
        return str(value).lower()
    elif t == str:
        return '"'+value.replace('"', '\\"')+'"'
    elif t == type(None):
        return "nil"
    elif t == dict:
        res = "{ "
        for k, v in value.items():
            res = res+"["+serialize( k )+"] = "+serialize( v )+", "
        res = res+" }"
        return res
    else:
        error( "Can't serialize a value of type "+str(t) )


def deserialize_data( s ):
    ds = s.replace(infStr, "float('inf')")
    ds = ds.replace(negInfStr, "-float('inf')")
    ds = ds.replace(nanStr, "float('nan')")

    ds = ds.replace('true', 'True')
    ds = ds.replace('false', 'False')

    ds = ds.replace('nil', 'None')
    ds = ds.replace('\\\n\9', '\\\n')

    try:
        ds = convert_lua_table_str_to_python_dict_str(ds)
        result = eval(ds)
        return result
    except BaseException as e:
        raise ProtocolException("Error deserializing message \n{}\n{}".format(s, e))


def convert_lua_table_str_to_python_dict_str(s):
    subbed_s = re.sub(r"\[(.+?)\]\s*=\s*([\w\W]*?[,{])", r"\g<1>: \g<2>", s) # NOTE: does not support keys with newlines, also expects all keys to be wrapped in []
    return re.sub(r":\s*\"([\w\W]*?)\"([,{])", r': """\g<1>"""\g<2>', subbed_s) # replace '= "X"' with '= """X"""'


def serialize_to_message(serialized_data, channel):
    return channel + '\n' + str(len(serialized_data)) + '\n' + serialized_data


def parse_grld_message(self, message):
    """
    returns parsed_message, remaining_buffer_data
    """
    if len(message) == 0:
        return '', ''

    if message.count("\n") < 2:
        raise ProtocolException("Tried to parse malformed GRLD data")

    channel, messageSize, remaining = message.split("\n", 2)
    data = remaining[:int(messageSize)]
    remaining = remaining[int(messageSize):]

    return data, remaining