"""Populate / extend the BandPass Filter table & documentation, and associated utilties

add_bpfilters has three modes of operation:

1. Add bp filters and generate associated spectra (documentation)
2. Add bp filters, without documentation
3. Scan the bp filters for duplicate wavelengths

In the first mode, the command takes two parameters:

1. A CSV file containing the bandpass filter information, see below
2. The root document directory (typically /path/to/asvo-tao/docs/)

By default, bandpass filter documentation is generated as described below.
This may be disabled with the --no-doco flag.

The input bandpass file is a CSV file with columns:

1. Filename
2. Label
3. Description

A spectra is produced for each filter and the Description is extended with a
link to the spectra in the documentation.

Existing file names have their label, description and spectra replaced.

Entries are never deleted (this currently needs to be done manually).

The bandpass filter documentation is generated with the following structure:

    /path/to/asvo-tao/docs/
        bpfilters/
            index.rst
            filter1.rst
            .
            .
            .
            filterN.rst
            spectra/
                filter1.png
                .
                .
                .
                filterN.png

Links to the documentation are assumed to be: [settings.STATIC_URL]/docs/bpfilters/filterM.html

When scanning the filters for duplicate wavelengths a single parameter is supplied:
the CSV file containing the bandpass filter information 
"""

import sys
import csv
import os
from os import listdir
from os.path import abspath, isdir, join, splitext, dirname
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

from tao.models import BandPassFilter
from utilities.plot_filter import plot_filter



class Command(BaseCommand):
    args = "<filters.csv filename> <doc root directory>"
    help = """Populate / extend the BandPass Filter table"""
    option_list = BaseCommand.option_list + (
        make_option("-d", action='store_true', default=False,
                    dest='debug',
                    help="Enter the debugger and halt"),
        make_option("--check-dups", action='store_true', default=False,
                    dest='checkdups',
                    help="Flag spectra with duplicate wavelengths and exit"),
        make_option("--no-doco", action='store_false', default=True,
                    dest='gendoco',
                    help="Disable the production and linking of bandpass spectra"),
        make_option("--doc", action='store_true', default=False,
                    dest='doc',
                    help="Display the command documentation and exit")
        )


    def handle(self, *args, **options):
        if options['doc']:
            print __doc__
            exit(0)
        self._args = args
        self._options = options
        if options['debug']:
            import pdb
            pdb.set_trace()
        if options['checkdups']:
            if len(args) != 1:
                raise CommandError("{0} <filters.csv filename> required".format(sys.argv[0]))
            self.check_dups()
            exit(0)
        if options['gendoco']:
            if len(args) != 2:
                raise CommandError("{0} <filters.csv filename> <doc root directory> required".format(sys.argv[0]))
        else:
            if len(args) != 1:
                raise CommandError("{0} <filters.csv filename> required".format(sys.argv[0]))

        if options['gendoco']:
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
            url_root = settings.STATIC_URL + 'docs/bpfilters/'
            for record in csvreader:
                #
                # Read the record
                #
                if len(record) < 2 or len(record) > 3:
                    raise CommandError("Expected 2 or 3 columns")
                print "Processing: {0}...".format(record[0])
                filter_fn = record[0].strip()
                label = record[1].strip()
                if len(record) == 3:
                    description = record[2].strip()
                else:
                    description = ''
                flattened_fn = filter_fn.replace(os.sep, '_')
                if self._options['gendoco']:
                    details = ("<p>{description}</p>\n"
                               "<p>Additional Details: <a href=\"{url_root}"
                               "{ffn}.html\">{label}</a>.</p>").format(
                                    description=description, url_root=url_root,
                                    ffn=flattened_fn, label=label)
                    spectra_fn = self.generate_spectra(filter_fn, flattened_fn, label, description)
                    self.generate_doco(filter_fn, flattened_fn, label, description, spectra_fn)
                else:
                    details = ("<p>{description}</p>\n").format(
                                    description=description)
                self.save_filter(filter_fn, label, details)
        if self._options['gendoco']:
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


    def check_dups(self):
        """Iterate over all the filters and flag if a duplicate wavelength is found"""
        csvfn = self._args[0]
        csv_root = dirname(csvfn) 
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
                filter_fn = record[0].strip()
                label = record[1].strip()
                bpfn = join(csv_root, filter_fn)
                previous = None
                with open(bpfn, 'r') as bpfile:
                    for filter in bpfile:
                        current = filter.split()[0]
                        if current == previous:
                            print "   duplicate wavelength: {0}".format(filter.strip())
                        previous = current
        return
