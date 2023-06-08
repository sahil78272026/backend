# import from django
from django.contrib import admin

# Local Import
from .models import *

# Register your models here.

# will return default object name in admin console
# admin.site.register(Student)

# to display fields of models
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','roll','city']