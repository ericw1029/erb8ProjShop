from import_export import resources
from .models import Category

class CategoryResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        row["name"] = f"{str(row['name']).strip():.{200}}"
        row["slug"] = f"{str(row['slug']).strip():.{200}}"
        super().before_import_row(row, **kwargs)

    class Meta:
        model = Category