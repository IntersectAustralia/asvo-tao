# coding: utf-8
"""TAO Metadata Management Utility

Note that this is a development utility and is expected to be used with care!

See --help for command formats.

The metadata xml file format:

<settings>
    <properties>
        <Field Type="int" DBFieldName="ObjectType">Type</Field>
        <Field Type="long long" DBFieldName="GlobalGalaxyID">GalaxyIndex</Field>                     
        <Field Type="int">HaloIndex</Field>
        <Field Type="int">FOFHaloIndex</Field>
        ...
    </properties>
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
from django.forms.models import model_to_dict

from tao.models import DataSet, DataSetProperty, Snapshot

_current_command = __name__.split('.')[-1]
moddoc = __doc__


class Command(NoArgsCommand):
    help = """
Manage DataSetProperty and Snapshot info in the specified DataSet

List available datasets:
    --list-available-datasets

Load property and snapshot info from the supplied file:
    --dataset=<dataset_id> --file=<filename>

Replace property info in dataset X from dataset Y:
    --dataset=<dataset X id> --replace-properties=<dataset Y id>

Update calculated property info in dataset X from dataset Y:
    --dataset=<dataset X id> --replace-snapshots=<dataset Y id>

Replace snapshot info in dataset X from dataset Y:
    --dataset=<dataset X id> --replace-snapshots=<dataset Y id>

Replace property attribute in dataset X from dataset Y:
    --dataset=<dataset X id> --replace-attribute=<dataset Y id> --attribute=<name>
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
            dest='replace_properties',
            default=None,
            help='replace dataset properties from the nominated dataset id',
        ),
        make_option('--update-calculated',
            type="int",
            action='store',
            dest='update_calculated',
            default=None,
            help='update calculated dataset properties from the nominated dataset id',
        ),
        make_option('--replace-snapshots',
            type="int",
            action='store',
            dest='replace_snapshots',
            default=None,
            help='replace dataset snapshots from the nominated dataset id',
        ),
        make_option('--replace-attribute',
            type="int",
            action='store',
            dest='replace_attribute',
            default=None,
            help='replace dataset property units from the nominated dataset id',
        ),
        make_option('--attribute',
            action='store',
            dest='attribute',
            default=None,
            help='attribute name to copy with --replace-attribute',
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
        elif options['replace_properties'] and options['dataset_id']:
            self._replace_properties(options['replace_properties'], options['dataset_id'])
        elif options['update_calculated'] and options['dataset_id']:
            self._update_calculated(options['update_calculated'], options['dataset_id'])
        elif options['replace_snapshots'] and options['dataset_id']:
            self._replace_snapshots(options['replace_snapshots'], options['dataset_id'])
        elif options['replace_attribute'] and options['attribute'] and options['dataset_id']:
            self._replace_attribute(options['replace_attribute'],
                                options['dataset_id'], options['attribute'])
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
        fields = tree.getroot().find('properties')
        for field in fields:
            data_type_name = field.attrib.get('Type', None)
            data_type = DataSetProperty.data_type_enum(data_type_name)
            label = field.text
            field_name = field.attrib.get('DBFieldName', label)
            is_computed = field.attrib.get('IsComputedField', False)
            is_filter = field.attrib.get('IsFilterField', True)
            is_output = field.attrib.get('IsOutputField', True)
            description = field.attrib.get('FieldDesc', '')
            units = field.attrib.get('Units', '')
            if int(self._options['verbosity']) >= 2:
                print("Adding {field}...".format(field=field_name))
            new_property = DataSetProperty(dataset=data_set,
                                           name=field_name,
                                           label=label,
                                           data_type=data_type,
                                           units=units,
                                           is_computed=is_computed,
                                           is_filter=is_filter,
                                           is_output=is_output,
                                           description=description)
            new_property.save()
        
        snapshots = Snapshot.objects.filter(dataset=data_set)
        snapshots.delete()
        
        redshifts = tree.getroot().find('snapshots')
        if redshifts is None:
            # redshifts are optional
            redshifts = []
        for redshift in redshifts:
            value = redshift.text
            new_redshift = Snapshot(dataset=data_set,
                                    redshift=value)
            new_redshift.save()

    @transaction.commit_on_success
    def _replace_properties(self, replace_properties, dataset_id):
        """Replace the dataset properties (dataset_id) from the specified 
        dataset (replace_properties)"""
        # Look up the two datasets, exit on dataset not found
        try:
            data_set = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % dataset_id)
        try:
            replace_set = DataSet.objects.get(pk=replace_properties)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % replace_properties)

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
                if int(self._options['verbosity']) > 1:
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
            prop = DataSetProperty.objects.get(pk=id)
            filters = DataSet.objects.filter(default_filter_field=prop)
            if len(filters) > 0:
                print("Untested...")
                import pdb; pdb.set_trace()
                for filter in filters:
                    print(u"Clearing default filter in: {0}".format(str(filter)))
                    filter.default_filter_field = None
                    filter.save()
            print("Deleting old property: {0}".format(str(prop)))
            prop.delete()


    @transaction.commit_on_success
    def _update_calculated(self, replace_id, dataset_id):
        """Update the calculated dataset properties (dataset_id) from the specified 
        dataset (replace_id).
        Any existing calculated properties are left unchanged."""
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
        # dataset properties.
        #
        properties = DataSetProperty.objects.filter(dataset=replace_set,
                                                    is_computed=True)
        i = 0
        for source_prop in properties:
            prop_id = source_prop.name
            existing_prop = DataSetProperty.objects.filter(
                dataset=data_set, name=prop_id)
            if len(existing_prop) == 1:
                existing_prop = existing_prop[0]
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
                if int(self._options['verbosity']) > 1:
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
        return

    @transaction.commit_on_success
    def _replace_snapshots(self, replace_snapshots, dataset_id):
        """Replace the dataset snapshots (dataset_id) from the specified 
        dataset (replace_snapshots)"""
        # Look up the two datasets, exit on dataset not found
        try:
            data_set = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % dataset_id)
        try:
            replace_set = DataSet.objects.get(pk=replace_snapshots)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % replace_snapshots)

        #
        # Copy the snapshots from the replacement set in to the target set
        #
        existing_snapshots = Snapshot.objects.filter(dataset=data_set)
        existing_snapshots.delete()
        snapshots = Snapshot.objects.filter(dataset=replace_set)
        for source_snapshot in snapshots:
            snapshot_dict = model_to_dict(source_snapshot, exclude=['id', 'dataset'])
            new_snapshot = Snapshot(**snapshot_dict)
            new_snapshot.dataset = data_set
            new_snapshot.save()
        return

    @transaction.commit_on_success
    def _replace_attribute(self, replace_id, dataset_id, attribute):
        """Replace the dataset property attribute (dataset_id) from the specified 
        dataset (replace_id).
        If the attribute exists in the source dataset but not the destination
        dataset it is ignored.
        If the attribute exists in the destination dataset but not the source
        dataset, it is left unchanged."""
        # Look up the two datasets, exit on dataset not found
        try:
            data_set = DataSet.objects.get(pk=dataset_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % dataset_id)
        try:
            replace_set = DataSet.objects.get(pk=replace_id)
        except DataSet.DoesNotExist:
            raise CommandError('DataSet not found: %s\n' % replace_id)
        # The property name can't be copied!
        assert attribute != 'name', "DataSetProperty name can't be copied"
        #
        # Copy the dataset property attribute from the replacement set in
        # to the target set
        #
        properties = DataSetProperty.objects.filter(dataset=replace_set)
        for property in properties:
            # Find the corresponding property in the target dataset
            dest_property = DataSetProperty.objects.filter(dataset=data_set,
                                                           name=property.name)
            assert len(dest_property) < 2, "Multiple properties with the same name found"
            if len(dest_property) == 0:
                continue
            # Copy the attribute from the source property in to the dest property
            new_val = getattr(property, attribute)
            if int(self._options['verbosity']) >= 2:
                print("Setting {attr} in {name} to {val}".format(attr=attribute,
                                                                 name=property.name,
                                                                 val=new_val))
            setattr(dest_property[0], attribute, new_val)
            dest_property[0].save()
        return
