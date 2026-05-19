from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



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
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("todo.urls")),

    path("api-auth/", include("rest_framework.urls")),

    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


