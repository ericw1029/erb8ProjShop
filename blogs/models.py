# models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Post(models.Model):
    """Example post model that comments can be attached to"""

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", args=[str(self.id)])


class Comment(models.Model):
    # Link to the user who posted the comment
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )

    # The comment content
    content = models.TextField()

    # Link to the post being commented on
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: Reply functionality
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    # Optional: Moderation fields
    is_approved = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]  # Oldest first for nested comments
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["post", "created_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        return self.post.get_absolute_url()
