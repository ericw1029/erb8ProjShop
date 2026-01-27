# urls.py (app-level)
from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "blogs"

urlpatterns = [
    # Post URLs
    path("", views.post_list, name="post_list"),
    path("post/search/", views.post_search, name="post_search"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    # Comment URLs
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/reply/", views.reply_comment, name="reply_comment"),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("comments/", views.comment_list, name="comment_list"),
]

"""
urlpatterns = [
    # Post URLs
    path("", views.post_list, name="post_list"),
    path(_("post/search/"), views.post_search, name="post_search"),
    path(_("post/new/"), views.post_create, name="post_create"),
    path(_("post/<int:post_id>/edit/"), views.post_edit, name="post_edit"),
    path(_("post/<int:post_id>/delete/"), views.post_delete, name="post_delete"),
    path(_("post/<int:post_id>/"), views.post_detail, name="post_detail"),
    # Comment URLs
    path(_("post/<int:post_id>/comment/"), views.add_comment, name="add_comment"),
    path(_("comment/<int:comment_id>/reply/"), views.reply_comment, name="reply_comment"),
    path(_("comment/<int:comment_id>/edit/"), views.edit_comment, name="edit_comment"),
    path(_("comment/<int:comment_id>/delete/"), views.delete_comment, name="delete_comment"),
    path(_("comments/"), views.comment_list, name="comment_list"),
]
"""

# Project-level urls.py (main urls.py)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # Your app name
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
]
"""
