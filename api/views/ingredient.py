# Djando Dependencies
from django.shortcuts import render

# Rest Framework Dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

# Models
from ..models import Ingredient

# Serializers
from ..serializers.ingredient import IngredientSerializer

#


class IngredientApiView(APIView):

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Ingredients
        '''
        ingredients = Ingredient.objects.filter()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Ingredient with given data
        - name(str): Name of the Ingredient
        '''
        data = {
            'name': request.data.get('name')
        }
        serializer = IngredientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
