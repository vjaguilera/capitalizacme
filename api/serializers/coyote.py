from rest_framework import serializers
from ..models import Coyote


class CoyoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coyote
        fields = ["name", "email"]
