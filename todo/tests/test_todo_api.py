import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from todo.models import Task

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestTaskViewSetList:
    """تست لیست تسکا"""

    def test_list_tasks_without_authentication(self, api_client):
        """بدون لاگین نباید ببینه"""
        url = reverse("todo:v1-app:tasks-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_tasks_with_authentication(self, authenticated_client, user, multiple_tasks):
        """با لاگین ببینه"""
        url = reverse("todo:v1-app:tasks-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_list_tasks_only_shows_user_tasks(self, authenticated_client, user):
        other_user = User.objects.create_user(
            email="other@example.com",
            full_name="Other User",
            password="pass123"
        )

        Task.objects.create(user=user, title="Task 1", is_done=False)
        Task.objects.create(user=user, title="Task 2", is_done=False)
        Task.objects.create(user=other_user, title="Other Task", is_done=False)

        url = reverse("todo:v1-app:tasks-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        
    def test_list_tasks_with_filter_is_done(self, authenticated_client, user):
        """فیلتر انجام شده"""
        Task.objects.create(user=user, title="Done Task", is_done=True)
        Task.objects.create(user=user, title="Pending Task", is_done=False)

        url = reverse("todo:v1-app:tasks-list")
        response = authenticated_client.get(url, {"is_done": True})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["is_done"] is True

    def test_list_tasks_with_search(self, authenticated_client, user):
        """جستجو با کلمه"""
        Task.objects.create(user=user, title="Django Project", is_done=False)
        Task.objects.create(user=user, title="Python Learning", is_done=False)
        Task.objects.create(user=user, title="Django Basics", is_done=False)

        url = reverse("todo:v1-app:tasks-list")
        response = authenticated_client.get(url, {"search": "Django"})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_list_tasks_ordering(self, authenticated_client, user):
        """مرتب سازی"""
        task1 = Task.objects.create(user=user, title="Task 1", is_done=False)
        task2 = Task.objects.create(user=user, title="Task 2", is_done=False)

        url = reverse("todo:v1-app:tasks-list")
        
        response = authenticated_client.get(url, {"ordering": "created_at"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == task1.id
        
        response = authenticated_client.get(url, {"ordering": "-created_at"})
        assert response.data[0]["id"] == task2.id


class TestTaskViewSetCreate:
    """تست ساختن تسک"""

    def test_create_task_without_authentication(self, api_client):
        """بدون لاگین نسازه"""
        url = reverse("todo:v1-app:tasks-list")
        data = {"title": "New Task", "description": "Test"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_task_with_authentication(self, authenticated_client, user):
        """با لاگین بسازه"""
        url = reverse("todo:v1-app:tasks-list")
        data = {
            "title": "New Task",
            "description": "Task description",
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Task"
        assert response.data["is_done"] is False
        assert Task.objects.filter(user=user).count() == 1

    def test_create_task_missing_title(self, authenticated_client):
        """عنوان نداشته باشه ارور بده"""
        url = reverse("todo:v1-app:tasks-list")
        data = {"description": "Task description"}
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_create_task_empty_title(self, authenticated_client):
        """عنوان خالی باشه قبول نکنه"""
        url = reverse("todo:v1-app:tasks-list")
        data = {"title": "", "description": "Task description"}
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_task_user_auto_assigned(self, authenticated_client, user):
        """خودکار کاربر رو بزنه روش"""
        url = reverse("todo:v1-app:tasks-list")
        data = {"title": "Auto User Task", "description": "Test"}
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        task = Task.objects.get(id=response.data["id"])
        assert task.user == user


class TestTaskViewSetRetrieve:
    """تست جزییات تسک"""

    def test_retrieve_task_without_authentication(self, api_client, task):
        """بدون لاگین نبینت"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_own_task(self, authenticated_client, task):
        """خودش بتونه ببینه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id
        assert response.data["title"] == task.title

    def test_retrieve_other_user_task(self, user, authenticated_client):
        """تسک دیگران رو نبینه"""
        other_user = User.objects.create_user(
            email="other@example.com",
            full_name="Other User",
            password="pass123"
        )
        other_task = Task.objects.create(
            user=other_user,
            title="Other Task",
            is_done=False
        )
        
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": other_task.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_nonexistent_task(self, authenticated_client):
        """تسکی که نیست رو 404 بده"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": 999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_task_has_detail_url(self, authenticated_client, task):
        """لینک جزییات داشته باشه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert "detail_url" in response.data
        assert response.data["detail_url"] is not None


class TestTaskViewSetUpdate:
    """تست ویرایش تسک"""

    def test_update_task_without_authentication(self, api_client, task):
        """بدون لاگین ویرایش نکنه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        data = {"title": "Updated"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_task(self, authenticated_client, task):
        """کمی ویرایش کنه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        data = {"title": "Updated Title"}
        response = authenticated_client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"
        assert response.data["description"] == task.description

    def test_full_update_task(self, authenticated_client, task):
        """کامل ویرایش کنه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        data = {
            "title": "Fully Updated",
            "description": "New description",
            "is_done": True
        }
        response = authenticated_client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Fully Updated"
        assert response.data["is_done"] is True

    def test_update_other_user_task(self, user, authenticated_client):
        """تسک دیگران رو ویرایش نکنه"""
        other_user = User.objects.create_user(
            email="other@example.com",
            full_name="Other User",
            password="pass123"
        )
        other_task = Task.objects.create(
            user=other_user,
            title="Other Task",
            is_done=False
        )
        
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": other_task.pk})
        data = {"title": "Hacked"}
        response = authenticated_client.patch(url, data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_created_at_readonly(self, authenticated_client, task):
        """تاریخ ساخته شدن عوض نشه"""
        original_created_at = task.created_at
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        data = {
            "title": "Updated",
            "created_at": "2020-01-01T00:00:00Z"
        }
        response = authenticated_client.patch(url, data)
        
        task.refresh_from_db()
        assert task.created_at == original_created_at


class TestTaskViewSetDelete:
    """تست حذف تسک"""

    def test_delete_task_without_authentication(self, api_client, task):
        """بدون لاگین حذف نکنه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_own_task(self, authenticated_client, user, task):
        """خودش بتونه حذف کنه"""
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": task.pk})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task.id).exists()

    def test_delete_other_user_task(self, user, authenticated_client):
        """تسک دیگران رو حذف نکنه"""
        other_user = User.objects.create_user(
            email="other@example.com",
            full_name="Other User",
            password="pass123"
        )
        other_task = Task.objects.create(
            user=other_user,
            title="Other Task",
            is_done=False
        )
        
        url = reverse("todo:v1-app:tasks-detail", kwargs={"pk": other_task.pk})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Task.objects.filter(id=other_task.id).exists()


class TestTaskViewSetActions:
    """تست اکشنای اضافی"""

    def test_toggle_complete_action(self, authenticated_client, task):
        """تغییر وضعیت انجام شده"""
        url = reverse("todo:v1-app:tasks-toggle-complete", kwargs={"pk": task.pk})
        
        assert task.is_done is False
        
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_done"] is True
        
        task.refresh_from_db()
        assert task.is_done is True
        
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_done"] is False

    def test_toggle_complete_without_authentication(self, api_client, task):
        """بدون لاگین عوض نکنه"""
        url = reverse("todo:v1-app:tasks-toggle-complete", kwargs={"pk": task.pk})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_other_user_task(self, user, authenticated_client):
        """تسک دیگران رو عوض نکنه"""
        other_user = User.objects.create_user(
            email="other@example.com",
            full_name="Other User",
            password="pass123"
        )
        other_task = Task.objects.create(
            user=other_user,
            title="Other Task",
            is_done=False
        )
        
        url = reverse("todo:v1-app:tasks-toggle-complete", kwargs={"pk": other_task.pk})
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestTaskSerializer:
    """تست سریالایزر"""

    def test_serializer_valid_data(self):
        """داده درست باشه اوکیه"""
        from todo.api.v1.serializers import TaskSerializer
        
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "is_done": False
        }
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_missing_required_field(self):
        """عنوان نباشه ارور بده"""
        from todo.api.v1.serializers import TaskSerializer
        
        data = {"description": "Test Description"}
        serializer = TaskSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_serializer_readonly_fields(self, user):
        """فیلدای فقط خوندنی عوض نشن"""
        from todo.api.v1.serializers import TaskSerializer
        from django.utils import timezone
        
        task = Task.objects.create(
            user=user,
            title="Test",
            description="Desc",
            is_done=False
        )
        original_created_at = task.created_at
        
        data = {
            "title": "Updated",
            "created_at": timezone.now()
        }
        serializer = TaskSerializer(task, data=data, partial=True)
        assert serializer.is_valid()
        serializer.save()
        
        task.refresh_from_db()
        assert task.created_at == original_created_at

    def test_serializer_fields(self, user):
        """فیلدا رو چک کنه"""
        from todo.api.v1.serializers import TaskSerializer
        
        task = Task.objects.create(
            user=user,
            title="Test",
            description="Desc",
            is_done=False
        )
        
        serializer = TaskSerializer(task, context={"request": None})
        data = serializer.data
        
        expected_fields = {"id", "title", "description", "is_done", "created_at", "detail_url"}
        assert set(data.keys()) == expected_fields