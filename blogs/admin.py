# admin.py
from django.contrib import admin
from .models import Post, Comment



class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "comment_count")
    list_filter = ("created_at", "author")
    search_fields = ("title", "content", "author__username")
    date_hierarchy = "created_at"

    def comment_count(self, obj):
        return obj.comments.count()

    comment_count.short_description = "Comments"

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "content_preview",
        "post",
        "created_at",
        "is_approved",
        "is_active",
    )
    list_filter = ("is_approved", "is_active", "created_at")
    search_fields = ("content", "author__username", "post__title")
    list_editable = ("is_approved", "is_active")
    actions = [
        "approve_comments",
        "disapprove_comments",
        "activate_comments",
        "deactivate_comments",
    ]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Content"

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_comments.short_description = "Disapprove selected comments"

    def activate_comments(self, request, queryset):
        queryset.update(is_active=True)

    activate_comments.short_description = "Activate selected comments"

    def deactivate_comments(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_comments.short_description = "Deactivate selected comments"
    
admin.site.register(Comment, CommentAdmin)
