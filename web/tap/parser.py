import re
from tao import models

def prepare_query(query):
    return query.replace('"', '').replace("'",'').replace("`",'')

def check_query(query):
    errors = ''
    if parse_dataset_name(query) == '':
        errors += "Dataset is not found.\n"
    if parse_fields(query) == '':
        errors += "Nothing to select.\n"
    if parse_joins(query) != []:
        errors += "Joins are not supported.\n"
    return errors

def parse_dataset_name(sql):
    regex = re.compile('(\s+FROM\s+(.*?)\s+?($|WHERE|ORDER|LIMIT))', re.I|re.M)
    found = regex.findall(sql)
    if found:
        split_definitions = re.compile('\s+AS\s+|\s+', re.I|re.M)
        dataset_description = re.split(split_definitions, found[0][1])
        label = ''
        if len(dataset_description) > 1:
            label = dataset_description[1]
        else:
            label = dataset_description[0]
        return {'name': dataset_description[0], 'label': label}
    else:
        return ''

# TODO: add units
def parse_fields(sql):
    fields = []
    regex = re.compile('^(SELECT\s+(.*?))(\s+FROM)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        split_fields = re.compile('\s?[,]\s?', re.I|re.M)
        split_definitions = re.compile('\s+AS\s+|\s+', re.I|re.M)
        for field in re.split(split_fields, found[0][1]):
            field_description = re.split(split_definitions, field)
            label = ''
            if len(field_description) > 1:
                label = field_description[1]
            else:
                label = field_description[0]
            fields.append({'value': field_description[0], 'label': label, 'units': ''})
            
    return fields

def parse_conditions(sql):
    regex = re.compile('(\s+WHERE\s(.*?)\s+?(GROUP BY|ORDER BY|LIMIT|\s+$))', re.I|re.M)
    found = regex.findall(sql)
    if found:
        regex = re.compile('\s+AND\s+', re.I|re.M)
        return re.split(regex, found[0][1])
    else:
        return []
    
def parse_order(sql):
    regex = re.compile('(ORDER\s+BY\s+(.*?))(\s+?LIMIT|\s+$)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        return found[0][1]
    else:
        return ''

def parse_limit(sql):
    regex = re.compile('(LIMIT\s+(.*))', re.I|re.M)
    found = regex.findall(sql)
    if found:
        return found[0][1]
    else:
        return ''
    
def parse_joins(sql):
    regex = re.compile('JOIN+', re.I|re.M)
    found = regex.findall(sql)
    if found:
        return found[0][1]
    else:
        return []
    