from django.urls import path, include
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskToggleDoneView,
    TaskListViewAPI
)

app_name = "todo"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("<int:pk>/toggle/", TaskToggleDoneView.as_view(), name="task_toggle"),
    path("api/v1/", include("todo.api.v1.urls")),

    # test to api
    path("todoapi/", TaskListViewAPI.as_view(), name="task_list_api"),
]
