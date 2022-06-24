# Djando Dependencies
import datetime as dt

# Rest Framework Dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.serializers.schedule_menu import ScheduleMenuSerializer

# Models
from ..models import Ingredient, Menu, PublicMenu, ScheduleMenu

# Serializers
from ..serializers.menu import MenuSerializer
from ..serializers.public_menu import PublicMenuSerializer

#


class MenuApiView(APIView):

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Menus
        '''

        menus = Menu.objects.filter()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Menu with given data
        - name(str): Name of the menu
        - code(str): Just a code to identify the Menu
        '''
        data = {
            'name': request.data.get('name'),
            'code': request.data.get('code')
        }
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailApiView(APIView):

    def get_object(self, menu_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return None

    # 1. Retrieve
    def get(self, request, menu_id, *args, **kwargs):
        '''
        Retrieves the Menu with given menu_id
        '''
        menu_instance = self.get_object(menu_id)
        if not menu_instance:
            return Response(
                {"res": "Object with menu id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MenuSerializer(menu_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicMenuApiView(APIView):

    permission_classes = [IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Public Menus avilables
        __Query Params__
        - start_date (datetime): Lower Bound to filter the available Menus, in format %Y-%m-%d
        - end_date (datetime): Upper Bound to filter the available Menus, in format %Y-%m-%d

        To filter for a specific date, just set the same start_date and end_date
        '''

        # Set the Query dict
        query = {}

        start_date = request.query_params.get('start_date')
        if start_date:
            # Add start date to the query as an lower bound
            query['pub_date__gte'] = dt.datetime.strptime(
                start_date, '%Y-%m-%d')
        end_date = request.query_params.get('end_date')
        if end_date:
            # Add end date to the query as an upper bound
            query['pub_date__lte'] = dt.datetime.strptime(end_date, '%Y-%m-%d')

        menus = PublicMenu.objects.filter(**query)
        serializer = PublicMenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Public Menu with given todo data
        - name(str): Name of the Public Menu
        '''
        data = {
            'name': request.data.get('name')
        }
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleMenuApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, menu_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return ScheduleMenu.objects.get(id=menu_id, user__id=user_id)
        except ScheduleMenu.DoesNotExist:
            return None

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Scheduled Menus related to a user
        '''
        query = {'user__id': request.user.id}
        menus = ScheduleMenu.objects.filter(**query)
        serializer = ScheduleMenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Scheduled Menu with given data
        __Query Params__
        - plate_id(int): Plate to be changed
        - public_menu_id: Public Menu Id to be changed
        '''
        data = {
            'plate_id': request.data.get('plate_id'),
            'public_menu_id': request.data.get('public_menu_id')
        }

        if data['public_menu_id'] is None:
            return Response('Public Menu Id is required', status=status.HTTP_400_BAD_REQUEST)

        if data['plate_id'] is None:
            return Response('Plate Id is required', status=status.HTTP_400_BAD_REQUEST)

        # Get Public Menu
        public_menu = PublicMenu.objects.get(id=data['public_menu_id'])
        # Create an Array of plates Id to check if the plate was available
        plates_id = [plate.id for plate in public_menu.menu.plates.all()]

        if int(data['plate_id']) not in plates_id:
            return Response('You have to choose a plate from the published Menu',
                            status=status.HTTP_400_BAD_REQUEST)

        # Schedule the Public Menu to the User
        data = {
            "pub_date": public_menu.pub_date,
            "plate": int(data['plate_id']),
            "user": request.user.id
        }
        serializer = ScheduleMenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleMenuDetailApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, menu_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return ScheduleMenu.objects.get(id=menu_id, user__id=user_id)
        except ScheduleMenu.DoesNotExist:
            return None

    # 1. Update
    def put(self, request, scheduled_menu_id, *args, **kwargs):
        '''
        Updates the Scheduled Menu Plate changing ingredients
        - new_ingredients(Array of int): Array with the new ingredients id of the scheduled plate
        '''
        scheduled_menu = self.get_object(scheduled_menu_id, request.user.id)
        if not scheduled_menu:
            return Response(
                {"res": "Object with scheduled menu id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Get new ingredients
        new_ingredients_id = request.data.get('new_ingredients_id')

        # If the user wants to remove all ingredients from the plate, denied it
        if len(new_ingredients_id) == 0:
            serializer = ScheduleMenuSerializer(scheduled_menu)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create an array of new ingredients id
        ingredients_id = [
            ingredient.id for ingredient in scheduled_menu.plate.ingredients.all()]

        # Check if the new ingredients exists in the plate's ingredients
        if not all(new_ingredient in ingredients_id for new_ingredient in new_ingredients_id):
            return Response('You cant set Ingredients that are currently not included in the Plate',
                            status=status.HTTP_400_BAD_REQUEST)

        # Copy the plate and change it to a personalized one
        copy_plate = scheduled_menu.plate
        copy_plate.pk = None
        copy_plate.personalized = True
        copy_plate.save()

        # Set the new ingredients
        new_ingredients = Ingredient.objects.filter(id__in=new_ingredients_id)

        copy_plate.ingredients.set(new_ingredients)
        copy_plate.save()

        # Update the scheduled plate
        scheduled_menu.plate = copy_plate
        scheduled_menu.save()

        serializer = ScheduleMenuSerializer(scheduled_menu)
        return Response(serializer.data, status=status.HTTP_200_OK)
