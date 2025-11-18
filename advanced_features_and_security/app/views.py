from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Post

# ---------------------------
# View Post
# ---------------------------
@permission_required('app.can_view', raise_exception=True)
def view_posts(request):
    posts = Post.objects.all()
    return render(request, "view_posts.html", {"posts": posts})


# ---------------------------
# Create Post
# ---------------------------
@permission_required('app.can_create', raise_exception=True)
def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        Post.objects.create(title=title, content=content)
        return redirect("view_posts")
    return render(request, "create_post.html")


# ---------------------------
# Edit Post
# ---------------------------
@permission_required('app.can_edit', raise_exception=True)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect("view_posts")
    return render(request, "edit_post.html", {"post": post})


# ---------------------------
# Delete Post
# ---------------------------
@permission_required('app.can_delete', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect("view_posts")
