from django.contrib import admin
from tao.models import Job, UserProfile, Simulation, GalaxyModel, DataSet, DataSetParameter, StellarModel

for model in (UserProfile, Simulation, Job, GalaxyModel, DataSetParameter, StellarModel):
    admin.site.register(model)


class DataSetParameterInline(admin.TabularInline):
    model = DataSetParameter
    extra = 3
    
    
class DataSetAdmin(admin.ModelAdmin):
    inlines = [DataSetParameterInline]
admin.site.register(DataSet, DataSetAdmin)

