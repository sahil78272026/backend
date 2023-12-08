# import from django
from django.contrib import admin

# Local Import
from .models import *

# Register your models here.

# will return default object name in admin console
# admin.site.register(Student)
admin.site.register(Cloth)
admin.site.register(NewUser)
admin.site.register(GeneratedPDF)
admin.site.register(Singer)
admin.site.register(Song)
admin.site.register(FuelType)
admin.site.register(CarModel)
admin.site.register(Recipe)

# to display fields of models
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','roll','city']

