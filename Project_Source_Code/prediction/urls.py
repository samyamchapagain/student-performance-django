from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.home, name="predict"),
    path("history/", views.history, name="history"),
    path("users/", views.users_list, name="users"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]