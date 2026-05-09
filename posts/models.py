from django.db import models
# Create your models here.

class Post(models.Model):
    """Post class"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField()
    is_published = models.BooleanField(default=True)
    user = models.IntegerField(null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(null=True,blank=True)

    def __str__(self) -> str:
        return f"({self.title} -- {self.content[:10]})"
    
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