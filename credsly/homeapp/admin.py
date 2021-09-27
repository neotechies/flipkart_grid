from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
class Admin(UserAdmin):
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff',
    'total_posts', 'total_friends', 'total_likes', 'total_comments',
    'total_followers', 'linkedin_zipname', 'facebook_zipname',
    'twitter_username', 'credit_score', 'total_credit'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('total_posts', 'total_friends', 'total_likes', 'total_comments',
            'total_followers', 'linkedin_zipname', 'facebook_zipname',
            'twitter_username', 'credit_score','total_credit')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('total_posts', 'total_friends', 'total_likes', 'total_comments',
            'total_followers', 'linkedin_zipname', 'facebook_zipname',
            'twitter_username', 'credit_score', 'total_credit')
        })
    )

admin.site.register(User, Admin)