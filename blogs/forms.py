# forms.py
from django import forms
from .models import Comment,Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "parent"]  # Include parent for replies
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your comment here...",
                    "maxlength": "1000",
                }
            ),
            "parent": forms.HiddenInput(),  # Hidden field for replies
        }
        labels = {
            "content": "Your Comment",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make parent field optional
        self.fields["parent"].required = False


class PostForm(forms.ModelForm):
    """Optional: Form for creating posts if needed"""

    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
