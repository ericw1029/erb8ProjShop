from django.contrib import admin
from .models import Category, Product
from import_export.admin import ImportExportModelAdmin
from .resources import CategoryResource

from django.urls import path
from .views import import_product_csv, export_products_csv

#@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    resource_class = CategoryResource

admin.site.register(Category, CategoryAdmin)


# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/', 
                self.admin_site.admin_view(import_product_csv), # Wrapped for security
                name='product-import-csv'
            ),

            path(
                'export-csv/', 
                self.admin_site.admin_view(export_products_csv), 
                name='product-export-csv'
            ),
        ]
        return custom_urls + urls
admin.site.register(Product, ProductAdmin)
