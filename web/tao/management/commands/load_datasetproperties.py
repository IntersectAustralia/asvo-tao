# coding: utf-8
"""Load / Replace the Properties (Fields) and Snapshots in to the specified DataSet.

Note that this is a development utility (hack) and isn't intended for production use.

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

class Command(NoArgsCommand):
    help = """
        add parameters to the specified DataSet

        usage:
            manage.py --list-available-datasets
        or:
            manage.py --dataset=<dataset_id> --file=<filename>

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
        make_option('--copy-properties',
            type="int",
            action='store',
            dest='copy_id',
            default=None,
            help='copy dataset properties from the nominated dataset id',
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
    )


    def handle_noargs(self, **options):
        if options['debug']:
            import pdb
            pdb.set_trace()
        if options['list_available_datasets']:
            self._list_available_datasets()
        elif options['xml_filename'] and options['dataset_id']:
            try:
                data_set = DataSet.objects.get(pk=options['dataset_id'])
            except DataSet.DoesNotExist:
                self.stderr.write('DataSet not found: %s\n' % options['dataset_id'])
                self._list_available_datasets()
            else:
                self._load_properties(data_set, options['xml_filename'])
        elif options['copy_id'] and options['dataset_id']:
            self._copy_properties(options['copy_id'], options['dataset_id'])
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
    def _copy_properties(self, copy_id, dataset_id):
        """Copy the dataset properties from the specified dataset"""
        try:
            data_set = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % dataset_id)
        try:
            copy_set = DataSet.objects.get(pk=copy_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % copy_id)

        properties = DataSetProperty.objects.filter(dataset=copy_set)
        i = 0
        for prop in properties:
            prop.dataset = data_set
            prop.pk = None
            prop.save()
            i += 1
        print("Copied {i} properties from {copy} to {dest}".format(
                i=i,
                copy=str(copy_set),
                dest=str(data_set)))
