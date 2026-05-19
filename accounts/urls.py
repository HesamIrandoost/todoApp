from django.urls import path, include
from .views import RegisterView, UserLoginView, UserLogoutView, send_email_view

app_name = "accounts"

urlpatterns = [
    path("send-email/", send_email_view),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    path("api/v1/", include("accounts.api.v1.urls")),
    path("api/v2/", include("djoser.urls")),
]
