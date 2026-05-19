from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from posts.form import PostForm, TestForm, CategoryForm, CatForm
from posts.models import Category, Post, Tag
from posts.posts import get_posts_filter_by_rate
from django.contrib.auth.decorators import login_required
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

def get_posts_by_category(request, id):
    category = Category.objects.filter(id = id).first()
    posts = category.posts.all()

    return render(request, template_name="posts/posts.html", context={"posts": posts, "category":category})

@login_required
def create_post(request: HttpRequest):

    if request.method == "POST":
        form = TestForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            tags = form.cleaned_data["tags"].split(" ")
            tag_objects = []
            tags_first = Tag.objects.all()

            for tag in tags:
                if not tags_first.filter(title=tag).exists():
                    tag_objects.append(Tag(title=tag))

            if tag_objects:
                Tag.objects.bulk_create(tag_objects)

            post = Post.objects.create(
                title=cleaned_data["title"],
                content=cleaned_data["content"],
                rate=cleaned_data["rate"],
                image=cleaned_data["image"],
                category_id=cleaned_data["category"],
                user = request.user,
            )
            created_tags = Tag.objects.filter(title__in=tags)
            post.tags.add(*created_tags)
        

            return redirect("posts")

        return render(request, "posts/create_post.html", context={"error": form.errors})

    form = PostForm()

    categories = Category.objects.all()

    return render(
        request,
        "posts/create_post.html",
        context={"form": form, "categories": categories},
    )


def edit_post(request: HttpRequest, pk):
    post = get_object_or_404(Post, id=pk)
    categories = Category.objects.all()
    if request.method == "POST":
        form = TestForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            post.title = cleaned_data["title"]
            post.content = cleaned_data["content"]
            post.rate = cleaned_data["rate"]
            if cleaned_data.get("image"):
                post.image = cleaned_data["image"]
            post.category_id = cleaned_data["category"]

            post.save()

            return redirect("post", id=post.pk)
        return render(
            request,
            "posts/edit_post.html",
            context={"post": post, "categories": categories, "errors": form.errors},
        )

    return render(
        request,
        "posts/edit_post.html",
        context={"post": post, "categories": categories},
    )


def delete_post(request: HttpRequest, id):

    if request.method == "GET":
        posts = get_object_or_404(Post, id=id)

        posts.delete()

        return redirect("posts")
    

def create_category(request: HttpRequest):

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            Category.objects.create(
                name=cleaned_data["name"],
            )
            return redirect("posts")

        return render(request, "categories/create_category.html", context={"error": form.errors})

    form = CatForm()

    return render(
        request,
        "categories/create_category.html",
        context={"form": form},
    )
