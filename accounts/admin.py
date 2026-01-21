from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "city", "created_at")
    list_filter = ("gender", "city", "country", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "city")
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "date_of_birth",
                    "gender",
                    "profile_image",
                )
            },
        ),
        ("Address Information", {"fields": ("address", "city", "country")}),
        ("Additional Information", {"fields": ("bio", "created_at", "updated_at")}),
    )

admin.site.register(Profile, ProfileAdmin)
