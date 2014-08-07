import re
from tao import models
<<<<<<< HEAD
=======
from tap.settings import FORBIDDEN, NOT_SUPPORTED
>>>>>>> work

def prepare_query(query):
    return query.replace('"', '').replace("'",'').replace("`",'').replace("\n",' ')

def check_query(query):
<<<<<<< HEAD
    errors = ''
    if not parse_dataset_name(query):
        errors += "Dataset is not found.\n"
    if len(parse_fields(query)) == 0:
        errors += "Nothing to select.\n"
    if len(parse_joins(query)) > 0:
        errors += "Joins are not supported.\n"
    return errors
=======
    for word in FORBIDDEN:
        regex = re.compile(r'\b%s\b' % word, re.I|re.M)
        found = regex.findall(query)
        if found:
            return "%s is forbidden." % word
    for word in NOT_SUPPORTED:
        regex = re.compile(r'\b%s\b' % word, re.I|re.M)
        found = regex.findall(query)
        if found:
            return "%s is not supported." % word
    if not parse_dataset_name(query):
        return "Dataset not found."
    if len(parse_fields(query)) == 0:
        return "Nothing to select."
    return ''
>>>>>>> work

def parse_dataset_name(sql):
    regex = re.compile('\s+FROM\s+(.*?)\s*?($|WHERE|ORDER|LIMIT|;)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        split_definitions = re.compile('\s+AS\s+|\s+', re.I|re.M)
        dataset = re.split(split_definitions, found[0][0])
        name = dataset[0].encode('utf-8')
        label = name
        if len(dataset) > 1:
            label = dataset[1].encode('utf-8')
        try:
<<<<<<< HEAD
            dataset = models.DataSet.objects.get(database=name, available=1)
            return {'name': name, 'label': label, 'simulation': dataset.simulation.name, 'galaxy_model': dataset.galaxy_model.name}
=======
            NameParts=name.split('__')
            qSimulationName= NameParts[0]
            qGalaxyModel=NameParts[1]       	        	
            #dataset = models.DataSet.objects.get(database=name, available=1)
            simultationobj=models.Simulation.objects.get(name=qSimulationName.replace('_','-'))
            galaxymodelobj=models.GalaxyModel.objects.get(name=qGalaxyModel)
            dataset = models.DataSet.objects.get(simulation=simultationobj.id,galaxy_model=galaxymodelobj.id, available=1)            
            return {'name':dataset.database , 'label': label, 'simulation': dataset.simulation.name, 'galaxy_model': dataset.galaxy_model.name}
>>>>>>> work
        except models.DataSet.DoesNotExist:
            pass

    return None

def parse_fields(sql, _dataset = None):
    dataset_id = None
    if _dataset:
        try:
            dataset = models.DataSet.objects.get(database=_dataset['name'])
            if dataset:
                dataset_id = dataset.id
        except models.DataSet.DoesNotExist:
            pass
<<<<<<< HEAD
=======

>>>>>>> work
        
    fields = []
    regex = re.compile('^(SELECT\s+TOP\s+[0-9]+\s+|SELECT\s+)(.*?)\s+FROM', re.I|re.M)   
    found = regex.findall(sql)
<<<<<<< HEAD
=======
    
    	    	
    
>>>>>>> work
    if found:
        split_fields = re.compile('\s?,\s?', re.I|re.M)
        field_labels = re.compile('\s*(.*?)(\s+AS\s+|\s+)(.*)', re.I|re.M)
        split_definitions = re.compile('\s+AS\s+|\s+', re.I|re.M)
        for field in re.split(split_fields, found[0][1]):
            name = label = field
            units = ''
            labels = field_labels.findall(field)
            if labels:
                name   = labels[0][0].encode('utf-8')
                label  = labels[0][2].encode('utf-8')
                if name == '':
                    name = label

            if dataset_id:
                try:
                    datatype = models.DataSetProperty.objects.get(dataset_id=dataset_id, name=name)
                    units = datatype.units.encode('utf-8')
                    if label == name:
                        label = datatype.label.encode('utf-8')
                except models.DataSetProperty.DoesNotExist:
                    pass
            
            fields.append({'value': name, 'label': label, 'units': units})
            
    return fields

def parse_conditions(sql):
    regex = re.compile('WHERE\s+(.*)\s*(GROUP BY|ORDER BY|LIMIT|;|$)', re.I|re.M|re.S)
    found = regex.findall(sql)
    conditions = []
    if found:
        # find all 'and' in 'between' statements
        regex = re.compile('AND\s+(.+BETWEEN\s+[0-9\.eE]+\s+AND\s+[0-9\.eE]+)', re.I)
        betweens = regex.findall(found[0][0])
        # separate and process the rest
        remaining_cond = regex.sub('', found[0][0])
        regex = re.compile('\s+AND\s+', re.I)
        conditions = re.split(regex, remaining_cond) + betweens
        
    return conditions
    
def parse_order(sql):
    regex = re.compile('(ORDER\s+BY\s+(.*?))\s*?(LIMIT|$|;)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        return found[0][1]
    else:
        return None

def parse_limit(sql):
    regex = re.compile('^SELECT\s+TOP\s+([0-9]+)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        return found[0]

    regex = re.compile('LIMIT\s+(.*)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        regex = re.compile('([0-9]+)\s?,\s*?([0-9]+)', re.I|re.M)
        pages = regex.findall(found[0])
        if pages and len(pages[0]) == 2:
            return pages[0][1]
        else:
            return found[0]
    
    return None
    
def parse_joins(sql):
    regex = re.compile('JOIN+', re.I|re.M)
    found = regex.findall(sql)
    if found:
        return found[0][1]
    else:
        return []
    
def remove_limits(sql):
    regex = re.compile('^SELECT\s+(TOP\s+[0-9]+)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        sql = sql.replace(found[0], '')

    regex = re.compile('(LIMIT\s+.*)', re.I|re.M)
    found = regex.findall(sql)
    if found:
        sql = sql.replace(found[0], '')

    while sql.find('  ') > 0:
        sql = sql.replace('  ', ' ')

    return sql
