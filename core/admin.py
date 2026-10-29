from django.contrib import admin
from .models import Booking
from import_export.admin import ImportExportModelAdmin

class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        'name',
        'mat_number',
        'department',
        'level',
        'has_paid',
        'timestamp'
    ]
    
    search_fields = [
        'name',
        'mat_number',
        'department',
        'level',
    ]
    
    list_filter = [
        'has_paid',
        'paid_when',
        'amount',
        'timestamp'
    ]
    
admin.site.register(Booking, BookingAdmin)