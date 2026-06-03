from rest_framework import serializers
from todo.models import Task
from rest_framework.reverse import reverse


class TaskSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "description", "is_done", "created_at", "detail_url"]
        read_only_fields = ["created_at"]

    def get_detail_url(self, obj):
        request = self.context.get("request")
        return reverse(
            "todo:v1-app:tasks-detail", kwargs={"pk": obj.pk}, request=request
        )


class HourlyWeatherSerializer(serializers.Serializer):
    time = serializers.ListField(child=serializers.CharField())
    temperature_2m = serializers.ListField(child=serializers.FloatField())

class WeatherForecastSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    timezone = serializers.CharField()
    hourly = HourlyWeatherSerializer()