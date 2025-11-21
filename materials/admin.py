from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'tutor', 'subject', 'material_type', 'created_at']
    list_filter = ['material_type', 'subject', 'created_at']
    search_fields = ['title', 'tutor__user__username']
