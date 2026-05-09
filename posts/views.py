from django.shortcuts import render, get_object_or_404
from posts.models import Post
from django.http import HttpResponse
from posts.posts import get_posts_filter_by_rate
# Create your views here.
def home(request):
    return render(request, "base.html")

def post(request):
    posts = get_posts_filter_by_rate(2)
    return render(request, template_name="posts/posts.html", context={"posts": posts})

def get_post(request, id):
    post = get_object_or_404(Post, id=id)

    return render(request, template_name="posts/post.html", context={"post": post})

def homework2(request):
    posts = Post.objects.filter(is_published = True, rate__gt = 5)
    return render(request, template_name="posts/posts.html", context={"posts": posts})
