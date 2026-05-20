from django.shortcuts import get_object_or_404
from posts.models import Category, Comment, Post


def get_posts_filter_by_rate(rate):
    posts = Post.objects.filter(rate__gt=rate).order_by("-view_count", "-created_at")
    return posts

def get_categories():
    return Category.objects.all()

def create_comment(post_id, text, user_id: int | None) -> Comment:
    post = get_object_or_404(Post, id=post_id)
    comment = Comment(text=text, post=post, user_id=user_id)
    comment.save()
    return comment