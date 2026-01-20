from import_export import resources
from .models import Post
from .models import Comment

class PostResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        row["title"] = f"{str(row['title']).strip():.{200}}"
        row["created_at"] = f"{str(row['created_at']).strip():.{15}}"
        row["updated_at"] = f"{str(row['updated_at']).strip():.{15}}"
        super().before_import_row(row, **kwargs)

    class Meta:
        model = Post
        widgets = {'created_at': {'format': '%Y-%m-%d'}, 'updated_at': {'format': '%Y-%m-%d'}}


class CommentResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        row["created_at"] = f"{str(row['created_at']).strip():.{15}}"
        row["updated_at"] = f"{str(row['updated_at']).strip():.{15}}"
        super().before_import_row(row, **kwargs)

    class Meta:
        model = Comment
        widgets = {'created_at': {'format': '%Y-%m-%d'}, 'updated_at': {'format': '%Y-%m-%d'}}
