from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import (
    User,
    Group,
    StudentProfile,
    TeacherProfile,
    Specialization,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "surname", "patronymic", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "role", "groups"),
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(StudentProfile)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ["user__name", "user__surname", "user__patronymic", "group__name"]


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__name", "user__surname", "user__patronymic"]


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    search_fields = ["name"]
