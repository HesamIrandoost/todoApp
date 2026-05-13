from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Task

app_name = "todo"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description"]
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["title", "description", "is_done"]
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("todo:task_list")

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "todo/task_confirm_delete.html"
    success_url = reverse_lazy("todo:task_list")

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user


class TaskToggleDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_done = not task.is_done
        task.save()
        return redirect("todo:task_list")
