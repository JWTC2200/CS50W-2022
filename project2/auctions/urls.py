from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listitem", views.create_listing, name="listitem"),
    path("item/<listing_id>", views.listing_view, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<category>", views.category, name="category"),
]
