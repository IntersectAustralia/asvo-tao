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

from tao.models import Job, Simulation, GalaxyModel, DataSet, DataSetProperty, StellarModel, Snapshot, BandPassFilter, DustModel, GlobalParameter, WorkflowCommand

for model in (GalaxyModel, StellarModel, BandPassFilter, DustModel, GlobalParameter):
    admin.site.register(model)

class SimulationAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'box_size_with_units')

admin.site.register(Simulation, SimulationAdmin)

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

class DataSetPropertyAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'label', 'is_filter', 'is_output', 'is_computed')
    ordering = ('dataset', 'group', 'order', 'label')

admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataSetProperty, DataSetPropertyAdmin)

class UserAdmin(AuthUserAdmin):
    """
    UserAdmin
    """

class JobAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user__username', 'status']

admin.site.register(Job, JobAdmin)

class WorkflowCommandAdmin(admin.ModelAdmin):
    model = WorkflowCommand
    readonly_fields = ('issued',)

admin.site.register(WorkflowCommand, WorkflowCommandAdmin)

admin.site.register(TaoUser, UserAdmin)
