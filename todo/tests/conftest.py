import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from todo.models import Task

User = get_user_model()


@pytest.fixture
def api_client():
    """API Client برای تست‌ها"""
    return APIClient()


@pytest.fixture
def user(db):  
    """کاربر نمونه - بدون username، با email و full_name"""
    return User.objects.create_user(
        email="test@example.com",
        full_name="Test User",  
        password="testpass123"
    )


@pytest.fixture
def admin_user(db):  
    """کاربر ادمین"""
    return User.objects.create_superuser(
        email="admin@example.com",
        full_name="Admin User",
        password="adminpass123"
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """API Client احراز‌شده"""
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    """API Client احراز‌شده ادمین"""
    token, _ = Token.objects.get_or_create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.fixture
def task(db, user):  
    """Task نمونه"""
    return Task.objects.create(
        user=user,
        title="تست Task",
        description="توضیحات تست",
        is_done=False
    )


@pytest.fixture
def multiple_tasks(db, user):  
    """چند Task نمونه"""
    tasks = []
    for i in range(5):
        task = Task.objects.create(
            user=user,
            title=f"Task {i+1}",
            description=f"توضیحات {i+1}",
            is_done=i % 2 == 0
        )
        tasks.append(task)
    return tasks