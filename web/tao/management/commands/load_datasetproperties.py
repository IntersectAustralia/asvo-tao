# coding: utf-8
"""Load / Replace the Properties (Fields) and Snapshots in the specified DataSet.

Note that this is a development utility and is expected to be used with care!

Example format:

<settings>
    <sageinput>
        <Field Type="int" DBFieldName="ObjectType">Type</Field>
        <Field Type="long long" DBFieldName="GlobalGalaxyID">GalaxyIndex</Field>                     
        <Field Type="int">HaloIndex</Field>
        <Field Type="int">FOFHaloIndex</Field>
        ...
    </sageinput>
    <snapshots>
        <redshift>0.0078125</redshift>
        <redshift>0.012346</redshift>
        <redshift>0.019608</redshift>
        ...
    </snapshots>
</settings>
"""

import xml.etree.ElementTree as ET
from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.db import transaction
from tao.models import DataSet, DataSetProperty, Snapshot

_current_command = __name__.split('.')[-1]
moddoc = __doc__


class Command(NoArgsCommand):
    help = """
Manage DataSetProperty and Snapshot info in the specified DataSet

List available datasets:
    manage.py --list-available-datasets

Load property and snapshot info from the supplied file:
    manage.py --dataset=<dataset_id> --file=<filename>

Replace property info in dataset X from the specified dataset Y:
    manage.py --dataset=<dataset_X> --replace-properties=<dataset_Y>
"""

    option_list = NoArgsCommand.option_list + (
        make_option('--list-available-datasets',
            action='store_true',
            dest='list_available_datasets',
            default=False,
            help='List available datasets',
        ),
        make_option('--file',
            action='store',
            dest='xml_filename',
            default=None,
            help='the input XML filename containing the metadata',
        ),
        make_option('--replace-properties',
            type="int",
            action='store',
            dest='replace_id',
            default=None,
            help='replace dataset properties from the nominated dataset id',
        ),
        make_option('--dataset',
            type="int",
            action='store',
            dest='dataset_id',
            default=None,
            help='the dataset which the new metadata applies to',
        ),
        make_option('--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='load pdb and halt after parsing options',
        ),
        make_option('--moddoc',
            action='store_true',
            dest='moddoc',
            default=False,
            help='print module doc and exit',
        ),
    )


    def handle_noargs(self, **options):
        self._options = options
        if options['debug']:
            import pdb
            pdb.set_trace()
        if options['list_available_datasets']:
            self._list_available_datasets()
        elif options['moddoc']:
            print moddoc
            print self.help
        elif options['xml_filename'] and options['dataset_id']:
            try:
                data_set = DataSet.objects.get(pk=options['dataset_id'])
            except DataSet.DoesNotExist:
                self.stderr.write('DataSet not found: %s\n' % options['dataset_id'])
                self._list_available_datasets()
            else:
                self._load_properties(data_set, options['xml_filename'])
        elif options['replace_id'] and options['dataset_id']:
            self._replace_properties(options['replace_id'], options['dataset_id'])
        else:
            self.stderr.write(self.help)

    def _list_available_datasets(self):
        self.stdout.write("Available Datasets:\n")
        for d in DataSet.objects.all():
            self.stdout.write("\tid: %s\t(%s)\n" % (d.id, d))

    @transaction.commit_on_success
    def _load_properties(self, data_set, xml_filename):
        """Replace the existing properties for the nominated dataset."""
        # Delete the existing properties
        properties = DataSetProperty.objects.filter(dataset=data_set)
        properties.delete()

        # Iterate over the supplied file and load the new properties
        tree = ET.ElementTree(file=xml_filename)
        fields = tree.getroot().find('sageinput')
        for field in fields:
            data_type_name = field.attrib.get('Type', None)
            data_type = DataSetProperty.data_type_enum(data_type_name)
            label = field.text
            field_name = field.attrib.get('DBFieldName', label)
            is_computed = field.attrib.get('IsComputedField', False)
            is_filter = field.attrib.get('IsFilterField', True)
            is_output = field.attrib.get('IsOutputField', True)
            description = field.attrib.get('FieldDesc', '')
            new_property = DataSetProperty(dataset=data_set,
                                           name=field_name,
                                           label=label,
                                           data_type=data_type,
                                           is_computed=is_computed,
                                           is_filter=is_filter,
                                           is_output=is_output,
                                           description=description)
            new_property.save()
        
        snapshots = Snapshot.objects.filter(dataset=data_set)
        snapshots.delete()
        
        redshifts = tree.getroot().find('snapshots')
        for redshift in redshifts:
            value = redshift.text
            new_redshift = Snapshot(dataset=data_set,
                                    redshift=value)
            new_redshift.save()

    @transaction.commit_on_success
    def _replace_properties(self, replace_id, dataset_id):
        """Replace the dataset properties (dataset_id) from the specified 
        dataset (replace_id)"""
        # Look up the two datasets, exit on dataset not found
        try:
            data_set = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % dataset_id)
        try:
            replace_set = DataSet.objects.get(pk=replace_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % replace_id)

        #
        # Copy the properties from the replacement set in to the target set
        #
        # We can't simply delete the old properties and replace due to the
        # default filter foreign key from the DataSet.
        #
        # Iterate over all the properties one by one and update the target
        # dataset properties.  Then delete any missed properties, as long
        # as they aren't part of the default filter.
        #
        properties = DataSetProperty.objects.filter(dataset=replace_set)
        existing_properties = DataSetProperty.objects.filter(dataset=data_set)
        existing_properties = [x.id for x in existing_properties]
        i = 0
        for source_prop in properties:
            prop_id = source_prop.name
            existing_prop = DataSetProperty.objects.filter(
                dataset=data_set, name=prop_id)
            if len(existing_prop) == 1:
                existing_prop = existing_prop[0]
                # Mark the property as processed
                existing_properties.remove(existing_prop.id)
            elif len(existing_prop) == 0:
                existing_prop = DataSetProperty(dataset=data_set)
            else:
                raise CommandError("Multiple properties found - should never get here")
            for field in source_prop._meta.fields:
                # Don't copy relations or the primary key
                if field.primary_key:
                    continue
                if field.rel is not None:
                    continue
                if self._options['verbosity'] > 1:
                    print(u"Set {name} from {old} to {new}".format(
                        name=field.name,
                        old=getattr(existing_prop, field.name),
                        new=getattr(source_prop, field.name)))
                setattr(existing_prop, field.name, getattr(source_prop, field.name))
            existing_prop.save()
            i += 1
        print("Replaced {i} properties from {replace} to {dest}".format(
                i=i,
                replace=str(replace_set),
                dest=str(data_set)))
        #
        # Delete any remaining properties from the target dataset.
        # If the property is a default filter, notify the user and
        # remove the filter
        #
        for id in existing_properties:
            print("Untested...")
            import pdb; pdb.set_trace()
            prop = DataSetProperty.objects.get(pk=id)
            filters = DataSet.objects.filter(default_filter_field=prop)
            if len(filters) > 0:
                for filter in filters:
                    print(u"Clearing default filter in: {0}".format(str(filter)))
                    filter.default_filter_field = None
                    filter.save()
            print("Deleting old property: {0}".format(str(prop)))
            prop.delete()
