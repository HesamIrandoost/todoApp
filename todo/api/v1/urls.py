from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "v1-app"

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")


# Swagger / Redoc   
schema_view = get_schema_view(
    openapi.Info(
        title="Todo API",
        default_version="v1",
        description="API Documentation for Todo App",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
