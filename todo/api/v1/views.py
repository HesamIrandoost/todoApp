from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from todo.models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["is_done", "created_at"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        task.is_done = not task.is_done
        task.save()
        return Response(
            {"id": task.id, "is_done": task.is_done}, status=status.HTTP_200_OK
        )
