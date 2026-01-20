from django.contrib import admin
from .models import Category, Product
from import_export.admin import ImportExportModelAdmin
from .resources import CategoryResource


#@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    resource_class = CategoryResource

admin.site.register(Category, CategoryAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

