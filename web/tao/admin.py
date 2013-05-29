"""
=============
tao.admin
=============
Provides few customisation classes and uses the admin API to register them. The
following models are made available in the admin site:

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from tao.models import TaoUser

from tao.models import Job, Simulation, GalaxyModel, DataSet, DataSetProperty, StellarModel, Snapshot, BandPassFilter, DustModel, GlobalParameter

for model in (Simulation, Job, GalaxyModel, DataSetProperty, StellarModel, BandPassFilter, DustModel, GlobalParameter):
    admin.site.register(model)


class DataSetPropertyInline(admin.TabularInline):
    """
    DataSetPropertyInLine
    """
    model = DataSetProperty
    extra = 3

class SnapshotInline(admin.TabularInline):
    """
    SnapshotInLine
    """
    model = Snapshot
    
class DataSetAdmin(admin.ModelAdmin):
    """
    DataSetAdmin
    """
    inlines = [DataSetPropertyInline, SnapshotInline]

admin.site.register(DataSet, DataSetAdmin)

class UserAdmin(AuthUserAdmin):
    """
    UserAdmin
    """

admin.site.register(TaoUser, UserAdmin)
