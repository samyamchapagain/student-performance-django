from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "user", "predicted_grade", "predicted_level",
        "math_score", "reading_score", "writing_score", "created_at")
    list_filter = ("predicted_grade", "predicted_level", "gender")
    search_fields = ("user__username", "gender", "ethnicity", "parental_education")
    autocomplete_fields = ("user",)


# Replace the default User admin with a clearer one so the
# "Users" section is easy to browse.
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "is_superuser", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)
