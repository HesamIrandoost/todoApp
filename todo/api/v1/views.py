from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from todo.models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

# Create your views here.
from rest_framework.authentication import TokenAuthentication


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["is_done", "created_at"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    
    @method_decorator(cache_page(60 * 13))
    @method_decorator(vary_on_headers("Authorization"))
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






import requests
from rest_framework.views import APIView
from .serializers import WeatherForecastSerializer



class WeatherForecastView(APIView):
    @method_decorator(cache_page(60 * 20))
    def get(self, request, *args, **kwargs):
        lat = request.query_params.get('lat', '35.6944')
        lon = request.query_params.get('lon', '51.4215')
        
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&timezone=auto&forecast_days=1"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status() 
            weather_data = response.json()
            
            serializer = WeatherForecastSerializer(data=weather_data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed weather data: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)