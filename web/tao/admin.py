"""
=============
tao.admin
=============
Provides few customisation classes and uses the admin API to register them. The
following models are made available in the admin site:

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from tao.models import Job, UserProfile, Simulation, GalaxyModel, DataSet, DataSetProperty, StellarModel, Snapshot, BandPassFilter

for model in (Simulation, Job, GalaxyModel, DataSetProperty, StellarModel, BandPassFilter):
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

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    """
    UserProfileInLine
    """
    model = UserProfile
    max_num = 1
    can_delete = False

class UserAdmin(AuthUserAdmin):
    """
    UserAdmin
    """
    inlines = [UserProfileInline]

admin.site.register(User, UserAdmin)
