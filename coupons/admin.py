from django.contrib import admin
from .models import Coupon
from import_export.admin import ImportExportModelAdmin
from .resources import CouponResource


#@admin.register(Coupon)
class CouponAdmin(ImportExportModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    resource_class = CouponResource


admin.site.register(Coupon, CouponAdmin)
