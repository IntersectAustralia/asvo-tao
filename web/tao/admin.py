from django.contrib import admin
from tao.models import Job, UserProfile, Simulation

for model in (UserProfile, Simulation, Job):
    admin.site.register(model)
