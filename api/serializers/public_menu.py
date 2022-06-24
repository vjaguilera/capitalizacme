from rest_framework import serializers
from ..models import PublicMenu


class PublicMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicMenu
        fields = ["id", "capacity", "pub_date", "menu"]
