# views.py
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.db.models import Q


# Post-related views
def post_search(request):
    queryset_list = Post.objects.order_by("-created_at")
    if "searchContent" in request.GET:
        search_content = request.GET["searchContent"]
        
        if search_content:
            queryset_list = queryset_list.filter(
                Q(title__icontains=search_content)
                | Q(content__icontains=search_content)
            )

    paginator = Paginator(queryset_list, 3)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    
    context = {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
    }
    return render(request, "blog/post_list.html", context)


def post_list(request):
    """Display list of posts"""
    posts_list = Post.objects.all().order_by("-created_at")

    # Pagination
    paginator = Paginator(posts_list, 3)  # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "posts": page_obj.object_list,
    }
    return render(request, "blog/post_list.html", context)

def post_detail(request, post_id):
    """Display a single post with its comments"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(is_active=True, is_approved=True, parent=None)

    # Handle comment submission
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "total_comments": post.comments.filter(
            is_active=True, is_approved=True
        ).count(),
    }
    return render(request, "blog/post_detail.html", context)

@login_required
def post_create(request):    
    """Create a new post"""
    if request.method == "POST":        
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("blogs:post_detail", post_id=post.id)
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "blog/post_form.html", context)

@login_required
def post_edit(request,post_id):
    
    post_item = Post.objects.get(id=post_id)
    form = PostForm(request.POST or None, instance=post_item)
    """Create a new post"""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("blogs:post_detail", post_id=post.id)
    
    context = {"form": form}
    return render(request, "blog/post_form.html", context)

@login_required
def post_delete(request,post_id):
    post_item = Post.objects.get(id=post_id)
    if request.method == "POST":
        title = post_item.title
        post_item.delete()
        messages.success(request, f'Post "{title}" deleted successfully.')
        return redirect("blogs:post_list")
    

# Comment-related views
@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect("blogs:post_detail", post_id=post.id)
    else:
        form = CommentForm()

    context = {
        "form": form,
        "post": post,
    }
    return render(request, "blogs/post_detail.html", context)

@login_required
def reply_comment(request, comment_id):
    """Reply to an existing comment"""
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.parent = parent_comment
            comment.save()
            messages.success(request, "Your reply has been posted!")
            return redirect("blogs:post_detail", post_id=post.id)
    else:
        # Pre-fill parent field
        form = CommentForm(initial={"parent": parent_comment.id})

    context = {
        "form": form,
        "post": post,
        "parent_comment": parent_comment,
    }
    return render(request, "blog/reply_comment.html", context)


@login_required
def edit_comment(request, comment_id):
    """Edit an existing comment"""
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if user owns the comment or is staff
    if not (request.user == comment.author or request.user.is_staff):
        return HttpResponseForbidden("You don't have permission to edit this comment.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect("blogs:post_detail", post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    context = {
        "form": form,
        "comment": comment,
        "post": comment.post,
    }
    return render(request, "blog/edit_comment.html", context)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment (soft delete)"""
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id

    # Check if user owns the comment or is staff
    if not (request.user == comment.author or request.user.is_staff):
        return HttpResponseForbidden(
            "You don't have permission to delete this comment."
        )

    # if request.method == "POST":
    if comment_id > 0:
        comment.is_active = False
        comment.save()
        messages.success(request, "Comment deleted successfully!")
        return redirect("blogs:post_detail", post_id=post_id)

    context = {
        "comment": comment,
    }
    return render(request, "blog/confirm_delete.html", context)


def comment_list(request):
    """Display all comments (for admin/moderation)"""
    comments = (
        Comment.objects.filter(is_active=True)
        .select_related("author", "post")
        .order_by("-created_at")
    )

    # Apply filters
    status = request.GET.get("status")
    if status == "approved":
        comments = comments.filter(is_approved=True)
    elif status == "pending":
        comments = comments.filter(is_approved=False)
    elif status == "rejected":
        comments = comments.filter(is_active=False)

    post_filter = request.GET.get("post")
    if post_filter:
        comments = comments.filter(post__title__icontains=post_filter)

    author_filter = request.GET.get("author")
    if author_filter:
        comments = comments.filter(author__username__icontains=author_filter)

    # Statistics for template
    approved_count = Comment.objects.filter(is_active=True, is_approved=True).count()
    pending_count = Comment.objects.filter(is_active=True, is_approved=False).count()
    deleted_count = Comment.objects.filter(is_active=False).count()
    total_count = Comment.objects.count()

    # Pagination
    paginator = Paginator(comments, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "comments": page_obj.object_list,
        "approved_count": approved_count,
        "pending_count": pending_count,
        "deleted_count": deleted_count,
        "total_count": total_count,
    }
    return render(request, "blog/comment_list.html", context)