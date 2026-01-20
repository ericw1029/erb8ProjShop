from import_export import resources
from .models import Coupon

class CouponResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        row["code"] = f"{str(row['code']).strip():.{50}}"
        row["valid_from"] = f"{str(row['valid_from']).strip():.{15}}"
        row["valid_to"] = f"{str(row['valid_to']).strip():.{15}}"
        super().before_import_row(row, **kwargs)

    class Meta:
        model = Coupon
        widgets = {'valid_from': {'format': '%Y-%m-%d'}, 'valid_to': {'format': '%Y-%m-%d'}}

