from django.contrib import admin
from .models import User_type, Region, Report_type, Pet_type, Pet_breed

# Register your models here.
admin.site.register(User_type)
admin.site.register(Region)
admin.site.register(Report_type)
admin.site.register(Pet_type)
admin.site.register(Pet_breed)