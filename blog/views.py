from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PostForm
from django.shortcuts import get_object_or_404
from .models import Post
from comments.forms import CommentForm

@login_required
def create_post_view(request):
    if not request.user.is_approved:
        messages.error(request, "Only approved users can create posts.")
        return redirect('accounts:login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post submitted! It will be visible once an admin approves it.")
            return redirect('blog:create_post')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})

def post_list_view(request):
    posts = Post.objects.filter(status=Post.Status.APPROVED)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.APPROVED)
    comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})