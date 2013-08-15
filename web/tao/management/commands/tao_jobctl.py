"""Overly simple command to manage the TAO MasterDB Job queue"""
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from optparse import make_option

from tao import models
from tao.models import Job, DataSet
from tao.models import TaoUser



class Command(BaseCommand):
    args = "<xml parameter file> <username> <database>"
    help = """CLI control of the TAO MasterDB Job queue
    
A few examples:

    Show all jobs:
        bin/django tao_jobctl --show=All
    Show jobs in progress:
        bin/django tao_jobctl --show=In_Progress
    Show status of selected job ids:
        bin/django tao_jobctl --show=All 123 124 125
    Re-run selected jobs:
        bin/django tao_jobctl --set_status=Submitted 123 124 125
    Submit a new job:
        bin/django tao_jobctl --status=Held --description="repetition={repetition}, iter={i}" --count=10 --repetition=Random lc.xml usrname millenniumm_full

Note that the description and xml parameter file can contain two variables as demonstrated above:

    i = current run number, from 1 to <count>
    repetition = Random or Unique
"""
    option_list = BaseCommand.option_list + (
        make_option("-d", action='store_true', default=False,
                    dest='debug',
                    help="Enter the debugger and halt"),
        make_option("--description", default='',
                    dest="description",
                    help="job description with i parameter"),
        make_option("--status", default="SUBMITTED",
                    dest='status',
                    help=('status: Held, Submitted, Queued, '
                          'In_Progress, Error, Completed.')),
        make_option("--count", default=1,
                    dest='count',
                    help=('the number of jobs to generate. '
                          'The current iteration is passed in as i')),
        make_option("--repetition", default="Random",
                    dest='repetition',
                    help=('the light-cone module repetition, default=Random')),
        make_option("--show", default=None,
                    dest='show',
                    help=('show the current queue, one of valid status or '
                          '"All" or "NotCompleted", with optional list of ids')),
        make_option("--set_status", default=None,
                    dest='set_status',
                    help=('set the status of the supplied list of ids'))
        )


    def handle(self, *args, **options):
        if options['debug']:
            import pdb
            pdb.set_trace()

        self.valid_states = [x[0] for x in models.STATUS_CHOICES]
        status = options['status'].upper()

        if options['show']:
            self.show_and_exit(*args, **options)

        if options['set_status']:
            self.set_status(*args, **options)
            sys.exit()

        # Crash if invalid status
        status_idx = self.check_state_name(status)
        description = options['description']
        fn = args[0]
        with open(fn, 'r') as fp:
            params = fp.read()
        username = args[1]
        # Crash if the user doesn't exist
        user = TaoUser.objects.get(username=username)
        database = args[2]
        if DataSet.objects.filter(database=database).count() != 1:
            raise CommandError("database '{db}' doesn't exist".format(db=database))
        repetition = options['repetition']
        if repetition not in ['Unique', 'Random']:
            raise CommandError("invalid repetition: {}".format(repetition))
        for j in range(int(options['count'])):
            i = j + 1
            new_job = Job(user=user,
                          description=description.format(i=i, repetition=repetition),
                          status=status,
                          database=database,
                          parameters=params.format(i=i, repetition=repetition)
                          )
            new_job.save()



    def show_and_exit(self, *args, **options):
        status = options['show'].upper()
        jobs = Job.objects.all()
        if len(args) > 0:
            jobs = jobs.filter(id__in=args)
        if status == 'NOTCOMPLETED':
            jobs = jobs.filter().exclude(status='COMPLETED').exclude(status='ERROR')
        elif status != 'ALL':
            # Check that a valid status has been requested
            self.check_state_name(status)
            jobs = jobs.filter(status=status)

        for job in jobs:
            print "{id} {user} {status} {description}".format(
                id=job.id,
                user=job.user.username,
                status=job.status,
                description=job.description[:48].replace(u"\n", u" "))
        sys.exit()



    @transaction.commit_on_success
    def set_status(self, *args, **options):
        status = options['set_status'].upper()
        # Check that a valid status has been requested
        self.check_state_name(status)
        jobs = Job.objects.filter(id__in=args)
        if jobs.count() != len(args):
            raise CommandError("Job ID mismatch: {jobs}".format(
                jobs=[x.id for x in jobs]))
        for job in jobs:
            job.status = status
            job.save()
        return


    def check_state_name(self, state):
        try:
            self.valid_states.index(state)
        except ValueError:
            print("Unknown state: {0} not in {1}".format(
                state, str(self.valid_states)))
            print("Or special state: All, NotCompleted")
            exit()
        return

