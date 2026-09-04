from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Add our custom field to the list view
    list_display = ('username', 'email', 'is_staff', 'is_approved')
    list_filter = ('is_staff', 'is_approved')

    # Add "is_approved" to the edit page, inside a new section
    fieldsets = UserAdmin.fieldsets + (
        ('Approval Status', {'fields': ('is_approved',)}),
    )

    # Also show it on the "Add user" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Approval Status', {'fields': ('is_approved',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)