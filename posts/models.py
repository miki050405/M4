from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=255)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Tag(models.Model):
    title = models.CharField(max_length=255)

class Post(models.Model):
    """Post class"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField()
    is_published = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL,related_name="posts",
    )

    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Posts"
        verbose_name_plural = "Post"

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"

    def __str__(self) -> str:
        return f"{self.name}"