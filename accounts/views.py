from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .models import User
from .forms import RegisterForm, LoginForm


from .tasks import sendmail

def send_email_view(request):
    sendmail.delay()
    return HttpResponse('<h1>done</h1>')

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
