# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, AdminProfile, StudentProfile, InstructorProfile, PartnerProfile


@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    
    def has_delete_permission(self, request, obj=None):
        # Customize the permission check here
        if request.user.is_superuser:
            return True
        else:
            return False

    model = CustomUser

    list_display = (
        
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                  
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "role"
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register([AdminProfile, StudentProfile, InstructorProfile, PartnerProfile])