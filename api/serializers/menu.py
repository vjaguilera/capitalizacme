from rest_framework import serializers
from ..models import Menu
from ..serializers.plate import PlateSerializer


class MenuSerializer(serializers.ModelSerializer):
    plates = PlateSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "plates"]
