from django.urls import path
from .views import *

urlpatterns = [
    path("profile",profile,name="profile"),
    path("todo/all_todos", show_all_todos, name="show_all_todos"),
    path("logout",logout_page,name="logout"),
    path("register",register,name = "register"),
    path("login",login_page,name="login"),
    path("todo",home,name="home"),
    path("todo/delete_item/<id>", delete_item, name="delete_item"),
    path("todo/update_status/<id>", update_status_to_finish, name="update_status_to_finish"),
    path("todo/update_status_to_progress/<id>", update_status_to_progress, name="update_status_to_progress"),
]
