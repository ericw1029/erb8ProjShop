from import_export import resources
from .models import Order

class OrderResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        row["first_name"] = f"{str(row['first_name']).strip():.{50}}"
        row["last_name"] = f"{str(row['last_name']).strip():.{50}}"
        row["email"] = str(row['email']).strip()
        row["address"] = f"{str(row['address']).strip():.{250}}"
        row["postal_code"] = f"{str(row['postal_code']).strip():.{20}}"
        row["city"] = f"{str(row['city']).strip():.{100}}"
        row["created"] = f"{str(row['created']).strip():.{15}}"
        row["updated"] = f"{str(row['updated']).strip():.{15}}"
        super().before_import_row(row, **kwargs)

    class Meta:
        model = Order
