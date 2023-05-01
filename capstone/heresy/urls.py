from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("builder", views.builder, name="builder"),
    path("unittotal", views.unit_total, name="unittotal"),
    path("savelist", views.savelist, name="savelist"),
    path("list_name_check", views.list_name_check, name="list_name_check"),
    path("damage", views.damage_page, name="damage"),
    path("damage_list", views.damage_list, name="damage_list"),
    path("damage_unit_pk", views.damage_unit_pk, name="damage_unit_pk"),
    path("damage_unit_stats", views.damage_load_unit_stats, name="damage_unit_stats"),
    path("list_view", views.list_view, name="list_view"),
    
]