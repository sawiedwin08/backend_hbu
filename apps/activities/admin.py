from django.contrib import admin
from apps.activities.models import *

# Register your models here.
class DimensionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class ProgramDimensionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class SubprogramDimensionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(Dimension, DimensionAdmin)
admin.site.register(ProgramDimension, ProgramDimensionAdmin)
admin.site.register(SubprogramDimension, SubprogramDimensionAdmin)
admin.site.register(Activity)
admin.site.register(AttandenceActivity)
