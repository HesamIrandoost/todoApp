from accounts.models import User
from rest_framework.test import APIClient


from django.urls import reverse


import pytest


@pytest.mark.django_db
class TestTodoApi:

    def setup_method(self):
        self.client = APIClient()
        self.data = {"title": "test", "is_done": False}

    def test_todo_api_401_response(self):
        url = reverse("todo:v1-app:tasks-list")
        response = self.client.get(url)
        assert response.status_code == 401

    def test_create_todo_api_201_status(self):
        user = User.objects.create_user(
            email="ajdadjadj@gmail.com", password="qwe123QWE@"
        )

        self.client.force_authenticate(user=user)
        url = reverse("todo:v1-app:tasks-list")
        response = self.client.post(url, self.data, format="json")

        assert response.status_code == 201

    def test_create_todo_api_status(self):
        url = reverse("todo:v1-app:tasks-list")
        response = self.client.post(url, self.data, format="json")

        assert response.status_code == 401
