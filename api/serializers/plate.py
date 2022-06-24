from rest_framework import serializers
from ..models import Plate
from ..serializers.ingredient import IngredientSerializer


class PlateSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(read_only=True, many=True)

    class Meta:
        model = Plate
        fields = ["id", "name", "ingredients"]
