def get_value(self, grld_id):
    with S.PROTOCOL as protocol:
        protocol.send('getValue')
        protocol.send(grld_id)
        response = protocol.read()

    return response

def is_table(self, variable):
    if type(variable) != dict: return False
    if 'value' not in variable: return False
    value = variable['value']
    if type(value) != dict: return False
    if 'type' not in value: return False

    return value['type'] == 'table'

def transform_grld_table(self, table_variable, parent_table_refs):
    name = table_variable['name']
    table_values = table_variable['value']
    table_ref = table_values['short']
    id = table_values['id']
    type = table_values['type']
    assert type == 'table', "table_variable passed to transform_grld_table must of type 'table'"

    parent_table_refs.append(table_ref)

    # TODO: create a command to fetch children
    table_children = {} # self.get_value(id)
    transformed_children = {}
    for i, child in table_children.items():

        if self.is_table(child):
            child_table_ref = child['value']['short']
            if child_table_ref in parent_table_refs: # special value if table child is a reference to the table itself (avoid infinite recursion)
                idx = parent_table_refs.index(child_table_ref)
                num_tables_up_from_child = len(parent_table_refs) - idx - 1
                if num_tables_up_from_child == 0:
                    description = '<circular reference to this table>'
                else:
                    description = '<circular reference to a parent table {} levels up>'.format(num_tables_up_from_child)

                transformed_children[i] =  {'name': child['name'], 'type':'table-ref', 'value': description}
            else:
                transformed_children[i] = self.transform_grld_variable(child, parent_table_refs)
        else:
            transformed_children[i] = self.transform_grld_variable(child, parent_table_refs)

    return {'name': name, 'type': type, 'value': table_ref, 'numchildren': len(transformed_children.keys()), 'children': transformed_children}

def transform_grld_variable(self, variable, parent_table_refs=None):
    name = variable['name']

    # if nothing is returned, GRLD returns {name = '<no result'>}
    if not 'value' in variable:
        return {'name': '', 'value': name, 'type': ''}

    if self.is_table(variable):
        return self.transform_grld_table(variable, parent_table_refs or []) #handle tables separately

    value = variable['value']
    if type(value) == dict:
        value_type = value['type']
        value = value['short']
    else:
        if type(value) == bool:
            value_type = 'boolean'
        elif type(value) == int or type(value) == float:
            value_type = 'number'
        elif type(value) == str:
            value_type = 'string'
        else:
            value_type = '?'

    return {'name': name, 'value': str(value), 'type': value_type}


def transform_grld_eval_response(self, eval_response, scope=None):
    transformed = {}
    for i, var in eval_response.items():
        transformed_item = self.transform_grld_variable(var)

        if scope:
            name = "(%s) %s" % (scope, transformed_item['name'])
            transformed_item['name'] = name
        else:
            name = transformed_item['name']

        transformed[i] = transformed_item

    return transformed


def transform_grld_context_response(self, context_response, scope):
    return self.transform_grld_eval_response(context_response, scope)