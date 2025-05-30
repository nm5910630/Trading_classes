from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(TrackedStock)
class TrackedStockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'company_name')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No image"
    
    image_preview.short_description = 'Image Preview'

admin.site.register(Testimonial)