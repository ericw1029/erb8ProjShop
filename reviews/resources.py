from import_export import resources
from .models import Review

class ReviewResource(resources.ModelResource):

    def before_import_row(created_at, row, **kwargs):
        row["created_at"] = f"{str(row['created_at']).strip():.{15}}"
        row["updated_at"] = f"{str(row['updated_at']).strip():.{15}}"
        super().before_import_row(row, **kwargs)

    class Meta:
        model = Review
        widgets = {'created_at': {'format': '%Y-%m-%d'}, 'updated_at': {'format': '%Y-%m-%d'}}
