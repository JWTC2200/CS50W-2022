
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<profile>", views.user, name="user"),
    path("following", views.following, name="following"),
    path("newpost", views.new_post, name="newpost"),
    path("likepost", views.likepost, name="likepost"),
    path("followed_posts", views.followed_posts, name="followed_posts")
]
