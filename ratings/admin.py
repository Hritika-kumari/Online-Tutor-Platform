from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student', 'tutor', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['student__user__username', 'tutor__user__username']
