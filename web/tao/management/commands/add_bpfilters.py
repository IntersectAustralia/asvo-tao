"""Populate / extend the BandPass Filter table

The input bandpass file is a CSV file with columns:

1. Filename
2. Label
3. Description

A spectra is produced for each filter and the Description is extended with a
link to the spectra in the documentation.

Existing file names have their label, description and spectra replaced.

Entries are never deleted (this needs to be done manually)."""

import sys
import csv
import os
from os import listdir
from os.path import abspath, isdir, join, splitext

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from optparse import make_option

from tao.models import BandPassFilter
from utilities.plot_filter import plot_filter



class Command(BaseCommand):
    args = "<filters.csv filename> <doc source directory>"
    help = """Populate / extend the BandPass Filter table"""
    option_list = BaseCommand.option_list + (
        make_option("-d", action='store_true', default=False,
                    dest='debug',
                    help="Enter the debugger and halt"),
        )


    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Command takes two arguments".format(sys.argv[0]))
        if options['debug']:
            import pdb
            pdb.set_trace()

        self._args = args
        self._options = options
        self._doc_dir = abspath(join(args[1], 'source', 'bpfilters'))
        if not isdir(self._doc_dir):
            raise CommandError("Doc dir not found: {0}".format(self._doc_dir))
        self._spectra_dir = join(self._doc_dir, 'spectra')
        if not isdir(self._spectra_dir):
            raise CommandError("Spectra dir not found: {0}".format(self._spectra_dir))
        self.populate_filters()


    @transaction.commit_on_success
    def populate_filters(self):
        """Process each entry in the filter file and then generate the index"""
        with open(self._args[0], 'r') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            csvreader = csv.reader(csvfile, dialect)
            for record in csvreader:
                #
                # Read the record
                #
                if len(record) < 2 or len(record) > 3:
                    raise CommandError("Expected 2 or 3 columns")
                print "Processing: {0}...".format(record[0])
                filter_fn = record[0]
                label = record[1]
                if len(record) == 3:
                    description = record[2].strip()
                else:
                    description = ''
                flattened_fn = filter_fn.replace(os.sep, '_')
                details = ("<p>{description}</p>\n"
                           "<p>Additional Details: <a href=\"/static/docs/"
                           "bpfilters/{ffn}.html\">{label}</a>.</p>").format(
                            description=description, ffn=flattened_fn, label=label)
                spectra_fn = self.generate_spectra(filter_fn, flattened_fn, label, description)
                self.generate_doco(filter_fn, flattened_fn, label, description, spectra_fn)
                self.save_filter(filter_fn, label, details)
        self.generate_index()


    def save_filter(self, filename, label, details):
                #
                # Insert / Update the record in the Master DB
                #
                bpfs = BandPassFilter.objects.filter(filter_id=filename)
                if len(bpfs) > 1:
                    # This should never happen
                    raise CommandError("Found multiple entries for {0}".format(filename))
                elif len(bpfs) == 1:
                    bpf = bpfs[0]
                    bpf.label = label
                    bpf.description = details
                else:
                    bpf = BandPassFilter(filter_id=filename,
                        label=label,
                        description=details)
                bpf.save()


    def generate_spectra(self, filename, flattened_fn, label, description):
        #
        # Produce the spectra image
        #
        dest = join(self._spectra_dir, flattened_fn + '.png')
        spectra_fn = plot_filter(filename, dest=dest)
        return spectra_fn

    
    def generate_doco(self, filename, flattened_fn, label, description, spectra_fn):
        fn = join(self._doc_dir, flattened_fn + '.rst')
        with open(fn, 'w') as fp:
            fp.write(label + '\n')
            # There must be a better way to do this...
            for i in range(0,len(label)):
                fp.write('=')
            fp.write('\n')
            fp.write(description)
            fp.write('\n\n')
            fp.write('.. image:: spectra/' + flattened_fn + '.png\n')
        return


    def generate_index(self):
        """Generate index.rst in the doco directory from all the other
        .rst files found"""
        index_fn = join(self._doc_dir, 'index.rst')
        with open(index_fn, 'w') as ifp:
            ifp.write("""BandPass Filters
================

.. toctree::
    :maxdepth: 1

""")
            dir_list = listdir(self._doc_dir)
            dir_list.sort()
            for file in dir_list:
                fn, ft = splitext(file)
                if file == 'index.rst' or ft != '.rst':
                    continue
                ifp.write("    " + fn + "\n")
        return
