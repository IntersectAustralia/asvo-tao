"""Quick and dirty script to populate / extend the BandPass Filter table"""
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from optparse import make_option

from tao.models import BandPassFilter



class Command(BaseCommand):
    args = "<bandpass file name...>"
    help = """Populate / extend the BandPass Filter table"""
    option_list = BaseCommand.option_list + (
        make_option("-d", action='store_true', default=False,
                    dest='debug',
                    help="Enter the debugger and halt"),
        )


    def handle(self, *args, **options):
        if options['debug']:
            import pdb
            pdb.set_trace()

        self.populate_filters(args, options)



    @transaction.commit_on_success
    def populate_filters(self, args, options):
        for filename in args:
            if filename.endswith(".dat"):
                filtername = filename[:-4]
            else:
                filtername = filename
            new_bpf = BandPassFilter(filter_id=filename,
                    label=filtername,
                    description="Please describe {fn}".format(fn=filtername))
            new_bpf.save()
        return

