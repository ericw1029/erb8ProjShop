from django.contrib import admin
from . models import Review
from import_export.admin import ImportExportModelAdmin
from .resources import ReviewResource

class ReviewAdmin(ImportExportModelAdmin):
  list_display = ("product", "user", "content", "rating", "created_at", "updated_at")
  resource_class = ReviewResource

admin.site.register(Review, ReviewAdmin)
# Register your models here.
