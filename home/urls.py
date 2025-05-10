from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("delete_item/<id>", delete_item, name="delete_item"),
    path("update_status/<id>", update_status_to_finish, name="update_status_to_finish"),
    path("update_status_to_progress/<id>", update_status_to_progress, name="update_status_to_progress"),
]
