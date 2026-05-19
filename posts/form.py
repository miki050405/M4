from django.forms import CharField, Form, ImageField, IntegerField, ModelForm
from django.core.exceptions import ValidationError
from posts.models import Post, Category


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "rate", "category", "image"]


class TestForm(Form):
    title = CharField(max_length=255, required=False)
    content = CharField(required=False)
    rate = IntegerField(min_value=1, max_value=10, required=False)
    category = IntegerField(required=False)
    image = ImageField(required=False)
    tags = CharField(required=False)

    def clean_title(self):
        test_title = self.cleaned_data['title']
        if test_title == "Запрещенное слово":
            raise ValidationError("Вы ввели запрещенное слово")
        
        return test_title

class CategoryForm(Form):
    name = CharField(max_length=255)

class CatForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']