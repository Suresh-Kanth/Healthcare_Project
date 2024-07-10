from django.contrib import admin
# from .models import Patient, Doctor,Blog
from .models import Users,Blog,Appointment

# Register your models here.

# admin.site.register(Patient)
# admin.site.register(Doctor)
admin.site.register(Users)
admin.site.register(Blog)
admin.site.register(Appointment)