from django.contrib import admin
from .models import Reservation

# admin.site.register(Reservation)

# Register your models here.

class Status(admin.ModelAdmin):  
    list_display = ('vehicle', 'user', 'status') 

admin.site.register(Reservation, Status)