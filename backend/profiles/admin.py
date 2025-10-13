from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Kursus


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('trainer_for', 'reg_number', 'account_number')


class KursusInline(admin.TabularInline):
    model = Kursus
    extra = 0
    fields = ('kursus', 'sted', 'arrangor', 'pris', 'file', 'created_at')
    readonly_fields = ('created_at',)


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, KursusInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Also register UserProfile separately for direct access
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'trainer_for', 'reg_number', 'account_number', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'trainer_for', 'reg_number', 'account_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Kursus)
class KursusAdmin(admin.ModelAdmin):
    list_display = ('user', 'kursus', 'sted', 'arrangor', 'pris', 'filename', 'created_at')
    list_filter = ('created_at', 'updated_at', 'sted', 'arrangor')
    search_fields = ('user__username', 'kursus', 'sted', 'arrangor')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
