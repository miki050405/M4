from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from posts.form import PostForm, CatForm
from posts.models import Category, Post, Tag, Comment
from posts.posts import create_comment, get_categories, get_posts_filter_by_rate
from django.contrib.auth.decorators import login_required
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

# Create your views here.
def home(request):
    return render(request, "base.html")

class GetPostListView(ListView):
    template_name = "posts/posts.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = get_posts_filter_by_rate(2)
        count = queryset.count()
        print(count)
        return queryset

class PostDetailView(DetailView):
    template_name = "posts/post.html"
    model = Post
    context_object_name = "post"

    def get_object(self, queryset: QuerySet[Any] | None = None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()
        return obj

class HomeWork2(ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"
    def get_queryset(self):
        return Post.objects.filter(is_published=True, rate__gt=5)

# def homework2(request):
#     posts = Post.objects.filter(is_published = True, rate__gt = 5)
#     return render(request, template_name="posts/posts.html", context={"posts": posts})


class PostsByCategory(ListView):
    template_name = "posts/posts.html"
    model = Post
    context_object_name = "posts"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

    def get_queryset(self):
        self.category = Category.objects.filter(id=self.kwargs["id"]).first()
        return self.category.posts.all()
    
    
    
# def get_posts_by_category(request, id):
#     category = Category.objects.filter(id = id).first()
#     posts = category.posts.all()
#     return render(request, template_name="posts/posts.html", context={"posts": posts, "category":category})


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["text"]

    def form_valid(self, form):
        user_id = self.request.user.id
        create_comment(
            post_id=self.kwargs["post_id"],
            text=form.cleaned_data["text"],
            user_id=user_id
        )
        return redirect("post", pk=self.kwargs["post_id"])

# def create_comment_view(request: HttpRequest, post_id):

#     if request.method == "POST":
#         user_id = None
#         if request.user:
#             user_id = request.user.id
#         comment = create_comment(post_id, request.POST.get("text"), user_id)

#         return redirect("post", post_id)
#     return redirect("post", post_id)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/create_post.html"
    form_class = PostForm
    success_url = reverse_lazy("posts")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = get_categories()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        tags = form.cleaned_data["tags"].split()
        tag_objects = []
        tags_first = Tag.objects.all()

        for tag in tags:
            if not tags_first.filter(title=tag).exists():
                tag_objects.append(Tag(title=tag))

        if tag_objects:
            Tag.objects.bulk_create(tag_objects)

        created_tags = Tag.objects.filter(title__in=tags)
        self.object.tags.add(*created_tags)

        return redirect("posts")

# @login_required
# def create_post(request: HttpRequest):

#     if request.method == "POST":
#         form = TestForm(request.POST, request.FILES)

#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             tags = form.cleaned_data["tags"].split(" ")
#             tag_objects = []
#             tags_first = Tag.objects.all()

#             for tag in tags:
#                 if not tags_first.filter(title=tag).exists():
#                     tag_objects.append(Tag(title=tag))

#             if tag_objects:
#                 Tag.objects.bulk_create(tag_objects)

#             post = Post.objects.create(
#                 title=cleaned_data["title"],
#                 content=cleaned_data["content"],
#                 rate=cleaned_data["rate"],
#                 image=cleaned_data["image"],
#                 category_id=cleaned_data["category"],
#                 user = request.user,
#             )
#             created_tags = Tag.objects.filter(title__in=tags)
#             post.tags.add(*created_tags)
        

#             return redirect("posts")

#         return render(request, "posts/create_post.html", context={"error": form.errors})

#     form = PostForm()

#     categories = Category.objects.all()

#     return render(
#         request,
#         "posts/create_post.html",
#         context={"form": form, "categories": categories},
#     )

class PostEdit(UpdateView):
    model = Post
    template_name = "posts/edit_post.html"
    form_class = PostForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = get_categories()
        return context
    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

# def edit_post(request: HttpRequest, pk):
#     post = get_object_or_404(Post, id=pk)
#     categories = Category.objects.all()
#     if request.method == "POST":
#         form = TestForm(request.POST, request.FILES)

#         if form.is_valid():
#             cleaned_data = form.cleaned_data

#             post.title = cleaned_data["title"]
#             post.content = cleaned_data["content"]
#             post.rate = cleaned_data["rate"]
#             if cleaned_data.get("image"):
#                 post.image = cleaned_data["image"]
#             post.category_id = cleaned_data["category"]

#             post.save()

#             return redirect("post", id=post.pk)
#         return render(
#             request,
#             "posts/edit_post.html",
#             context={"post": post, "categories": categories, "errors": form.errors},
#         )

#     return render(
#         request,
#         "posts/edit_post.html",
#         context={"post": post, "categories": categories},
#     )

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy("posts")

# def delete_post(request: HttpRequest, id):
#     if request.method == "GET":
#         posts = get_object_or_404(Post, id=id)
#         posts.delete()
#         return redirect("posts")
    
class CategoryCreate(CreateView):
    model = Category
    template_name = "categories/create_category.html"
    form_class = CatForm
    success_url = reverse_lazy("posts")

# def create_category(request: HttpRequest):
#     if request.method == "POST":
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             Category.objects.create(
#                 name=cleaned_data["name"],
#             )
#             return redirect("posts")
#         return render(request, "categories/create_category.html", context={"error": form.errors})
#     form = CatForm()
#     return render(
#         request,
#         "categories/create_category.html",
#         context={"form": form},
#     )
