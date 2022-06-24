# Djando Dependencies
from django.shortcuts import render

# Rest Framework Dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

# Models
from ..models import Plate

# Serializers
from ..serializers.plate import PlateSerializer

#


class PlateApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Plates
        '''
        plates = Plate.objects.filter()
        serializer = PlateSerializer(plates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Plate with given todo data
        '''
        data = {
            'name': request.data.get('name')
        }
        serializer = PlateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlateDetailApiView(APIView):

    def get_object(self, plate_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Plate.objects.get(id=plate_id)
        except Plate.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, plate_id, *args, **kwargs):
        '''
        Retrieves the Plate with given Plate_id
        '''
        plate_instance = self.get_object(plate_id)
        if not plate_instance:
            return Response(
                {"res": "Object with Plate id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PlateSerializer(plate_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class PlateDetailApiView(APIView):
#     # add permission to check if user is authenticated
#     # permission_classes = [permissions.IsAuthenticated]

#     def get_object(self, todo_id, user_id):
#         '''
#         Helper method to get the object with given todo_id, and user_id
#         '''
#         try:
#             return Todo.objects.get(id=todo_id, user = user_id)
#         except Todo.DoesNotExist:
#             return None

#     # 3. Retrieve
#     def get(self, request, todo_id, *args, **kwargs):
#         '''
#         Retrieves the Todo with given todo_id
#         '''
#         todo_instance = self.get_object(todo_id, request.user.id)
#         if not todo_instance:
#             return Response(
#                 {"res": "Object with todo id does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = TodoSerializer(todo_instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # 4. Update
#     def put(self, request, todo_id, *args, **kwargs):
#         '''
#         Updates the todo item with given todo_id if exists
#         '''
#         todo_instance = self.get_object(todo_id, request.user.id)
#         if not todo_instance:
#             return Response(
#                 {"res": "Object with todo id does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         data = {
#             'task': request.data.get('task'),
#             'completed': request.data.get('completed'),
#             'user': request.user.id
#         }
#         serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # 5. Delete
#     def delete(self, request, todo_id, *args, **kwargs):
#         '''
#         Deletes the todo item with given todo_id if exists
#         '''
#         todo_instance = self.get_object(todo_id, request.user.id)
#         if not todo_instance:
#             return Response(
#                 {"res": "Object with todo id does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         todo_instance.delete()
#         return Response(
#             {"res": "Object deleted!"},
#             status=status.HTTP_200_OK
#         )
