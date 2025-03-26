'''
This is the first code
'''

from django.contrib import admin
from .models import CustomUser, UserImage

@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at', 'verification_status')
    list_filter = ('verification_status', 'camera_make')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    actions = ['mark_verified', 'mark_rejected']
    
    def mark_verified(self, request, queryset):
        queryset.update(verification_status='verified')
    mark_verified.short_description = "Mark selected images as verified"
    
    def mark_rejected(self, request, queryset):
        queryset.update(verification_status='rejected')
    mark_rejected.short_description = "Mark selected images as rejected"

admin.site.register(CustomUser)