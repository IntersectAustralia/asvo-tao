from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from tao.models import Job, UserProfile, Simulation, GalaxyModel, DataSet, DataSetProperty, StellarModel, Snapshot

for model in (Simulation, Job, GalaxyModel, DataSetProperty, StellarModel):
    admin.site.register(model)


class DataSetPropertyInline(admin.TabularInline):
    model = DataSetProperty
    extra = 3

class SnapshotInline(admin.TabularInline):
    model = Snapshot
    
    
class DataSetAdmin(admin.ModelAdmin):
    inlines = [DataSetPropertyInline, SnapshotInline]
admin.site.register(DataSet, DataSetAdmin)


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]
admin.site.register(User, UserAdmin)
