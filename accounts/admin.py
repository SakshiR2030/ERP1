from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Student, ConcessionApplication

# -----------------------------
# CustomUser Admin
# -----------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "full_name", "is_staff", "is_active")
    search_fields = ("username", "email", "full_name")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "full_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "full_name", "password1", "password2", "is_staff", "is_active")}
        ),
    )


# -----------------------------
# Student Admin
# -----------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "branch", "year"]
    list_filter = ["branch", "year"]
    search_fields = ["user__username", "full_name"]


# -----------------------------
# ConcessionApplication Admin
# -----------------------------
@admin.register(ConcessionApplication)
class ConcessionApplicationAdmin(admin.ModelAdmin):
    list_display = ["student", "class_type", "period", "line", "from_station", "to_station", "applied_at"]
    list_filter = ["class_type", "period", "line", "applied_at"]
    search_fields = ["student__user__username", "from_station", "to_station"]
