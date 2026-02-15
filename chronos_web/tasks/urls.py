from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:task_id>/", views.detail, name="detail"),
    path("update-status/", views.update_status, name="update_status"),
    path("create/", views.create_task, name="create"),
    path("create2/", views.create_task2, name="create2"),
]
