from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from blog.models import Post
from .forms import CommentForm


@login_required
def add_comment_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.APPROVED)

    if not request.user.is_approved:
        messages.error(request, "Only approved users can post comments.")
        return redirect('blog:post_detail', pk=post.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted.")
        else:
            messages.error(request, "Comment could not be posted. Please try again.")

    return redirect('blog:post_detail', pk=post.pk)