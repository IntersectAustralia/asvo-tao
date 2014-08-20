"""
=============
tao.admin
=============
Provides few customisation classes and uses the admin API to register them. The
following models are made available in the admin site:

"""

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from tao.models import TaoUser

from tao.models import Job, Simulation, GalaxyModel, DataSet, DataSetProperty, StellarModel, Snapshot, BandPassFilter, DustModel, GlobalParameter, WorkflowCommand, SurveyPreset, format_human_readable_file_size
from tao.models import Catalogue,PreMade_DataSet,PreMade_DataSetProperty
for model in (GalaxyModel, StellarModel, BandPassFilter, DustModel, GlobalParameter, SurveyPreset):
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
    search_fields = ['id', 'name', 'label']

admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataSetProperty, DataSetPropertyAdmin)



class CatalogueAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

admin.site.register(Catalogue, CatalogueAdmin)
class PreMade_DataSetPropertyInline(admin.TabularInline):
    """
    PreMade_DataSetPropertyInLine
    """
    model = PreMade_DataSetProperty
    extra = 3
class PreMade_DataSetAdmin(admin.ModelAdmin):
    """
    PreMade_DataSetAdmin
    """
    inlines = [PreMade_DataSetPropertyInline]
    


class PreMade_DataSetPropertyAdmin(admin.ModelAdmin):
    list_display = ('PreMade_dataset', 'label', 'is_filter', 'is_output', 'is_computed')
    ordering = ('PreMade_dataset', 'group', 'order', 'label')
    search_fields = ['id', 'name', 'label']

admin.site.register(PreMade_DataSet, PreMade_DataSetAdmin)
admin.site.register(PreMade_DataSetProperty, PreMade_DataSetPropertyAdmin)



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = TaoUser

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['disk_quota'].help_text = "Value is in MB"

    def clean_password(self):
        return self.initial['password']


class UserAdmin(AuthUserAdmin):
    """
    UserAdmin
    """
    form = UserChangeForm
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_display = AuthUserAdmin.list_display + ('disk_quota',)
    fieldsets = AuthUserAdmin.fieldsets + ((_('Disk quota'), {'fields': ('disk_quota',)}),)
    readonly_fields = AuthUserAdmin.readonly_fields + ('username',)

class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('display_disk_usage',)

    def display_disk_usage(self, instance):
        return instance.display_disk_size()
    display_disk_usage.short_description = 'Disk usage'
    exclude = ('disk_usage',)
    search_fields = ['id', 'user__username', 'status', 'description']
    

admin.site.register(Job, JobAdmin)

class WorkflowCommandAdmin(admin.ModelAdmin):
    model = WorkflowCommand
    readonly_fields = ('issued',)
    search_fields = ['id', 'job_id', 'command', 'execution_status']

admin.site.register(WorkflowCommand, WorkflowCommandAdmin)

admin.site.register(TaoUser, UserAdmin)
