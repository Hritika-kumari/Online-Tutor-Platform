from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['student', 'tutor', 'subject', 'date', 'start_time', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['student__user__username', 'tutor__user__username']
    date_hierarchy = 'date'
