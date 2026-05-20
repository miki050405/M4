"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from posts.views import (
    home,
    PostCreateView,
    PostDelete,
    PostEdit,
    PostDetailView,
    PostsByCategory,
    GetPostListView,
    CategoryCreate,
    HomeWork2,
    CommentCreate,
)
from users.views import (
    login_user,
    logout_user,
    CreateUserView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('posts/',GetPostListView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name = 'post'),
    path('posts/hw2/',HomeWork2.as_view(), name = 'homework2'),
    path("posts/category/<int:id>/", PostsByCategory.as_view(), name="category"),
    path("posts/create/", PostCreateView.as_view(), name="create_post"),
    path("posts/<int:pk>/edit/", PostEdit.as_view(), name="edit_post"),
    path("posts/<int:pk>/delete", PostDelete.as_view(), name="delete_post"),
    path("categories/create/", CategoryCreate.as_view() , name = 'create_category'),
    path("user/login/",login_user,name="login"),
    path("user/logout/",logout_user,name="logout"),
    path("user/register/", CreateUserView, name="register"),
    path("posts/<int:post_id>/comment", CommentCreate.as_view(), name="create_comment"), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)