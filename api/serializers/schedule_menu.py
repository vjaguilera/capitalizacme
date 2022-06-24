from rest_framework import serializers
from ..models import ScheduleMenu


class ScheduleMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleMenu
        fields = ["id", "plate", "pub_date", "user"]
