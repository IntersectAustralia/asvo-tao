from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from tao.models import Job, UserProfile, Simulation, GalaxyModel, DataSet, DataSetParameter, StellarModel, Snapshot

for model in (Simulation, Job, GalaxyModel, DataSetParameter, StellarModel):
    admin.site.register(model)


class DataSetParameterInline(admin.TabularInline):
    model = DataSetParameter
    extra = 3

class SnapshotInline(admin.TabularInline):
    model = Snapshot
    
    
class DataSetAdmin(admin.ModelAdmin):
    inlines = [DataSetParameterInline, SnapshotInline]
admin.site.register(DataSet, DataSetAdmin)


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]
admin.site.register(User, UserAdmin)
