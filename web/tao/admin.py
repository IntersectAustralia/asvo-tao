from django.contrib import admin
from tao.models import Job, UserProfile, Simulation, GalaxyModel

for model in (UserProfile, Simulation, Job, GalaxyModel):
    admin.site.register(model)
