# coding: utf-8
import csv

from django.core.management.base import NoArgsCommand, CommandError
from django.db import transaction

from optparse import make_option

from tao.models import DataSet, DataSetParameter

_current_command = __name__.split('.')[-1]

class Command(NoArgsCommand):
    help = """
        add parameters to the specified DataSet

        usage:
            bin/django %s --list-available-datasets
        or:
            bin/django %s --dataset=<dataset_id> --csvfile=<filename>

""" % (_current_command, _current_command)

    option_list = NoArgsCommand.option_list + (
        make_option('--list-available-datasets',
            action='store_true',
            dest='list_available_datasets',
            default=False,
            help='List available datasets',
        ),
        make_option('--csvfile',
            action='store',
            dest='csv_filename',
            default=None,
            help='the input CSV filename containing label, units, column name',
        ),
        make_option('--dataset',
            type="int",
            action='store',
            dest='dataset_id',
            default=None,
            help='List available datasets',
        ),
    )


    def handle_noargs(self, **options):
        if options['list_available_datasets']:
            self._list_available_datasets()
        elif options['csv_filename'] and options['dataset_id']:
            try:
                data_set = DataSet.objects.get(pk=options['dataset_id'])
            except DataSet.DoesNotExist:
                self.stderr.write('DataSet not found: %s\n' % options['dataset_id'])
                self._list_available_datasets()
            else:
                self._add_parameters_to_data_set(data_set, options['csv_filename'])
        else:
            self.stderr.write(self.help)

    def _list_available_datasets(self):
        self.stdout.write("Available Datasets:\n")
        for d in DataSet.objects.all():
            self.stdout.write("\tid: %s\t(%s)\n" % (d.id, d))

    @transaction.commit_on_success
    def _add_parameters_to_data_set(self, data_set, csv_filename):
        with open(csv_filename) as csvparams:
            reader = csv.reader(csvparams)
            for (label, units, name) in reader:
                DataSetParameter(dataset=data_set, label=label, name=name, units=units).save()
