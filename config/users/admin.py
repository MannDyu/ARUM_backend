from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, RefreshTokenModel
from django.contrib import admin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

class RefreshTokenInline(admin.StackedInline):
    model = RefreshTokenModel
    can_delete = False
    verbose_name_plural = "refresh_token"

class UserAdmin(BaseUserAdmin):
    inlines = (RefreshTokenInline, ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
