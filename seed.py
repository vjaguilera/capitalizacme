from django.contrib.auth.models import User
import random
from randomuser import RandomUser
import os
import django
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
grandparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(grandparentdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acme.settings")
django.setup()

from api.models import (  # noqa: E402
    Ingredient,
    Plate,
    Menu,
    PublicMenu,
    ScheduleMenu,
)


INGREDIENTS = [
    # PROTEINAS
    "Pollo Asado", "Pollo Frito", "Pollo Cocido", "Carne Asada", "Carne al Jugo",
    "Pescado Frito", "Pescado a la Mantequilla", "Cerdo Apanado", "Cerdo teriyaki",
    "Cerdo asado", "Pavo cocido", "Pavo al vapor",
    # SALSAS,
    "Salsa huancaina", "Guacamole", "Salsa picante", "Salsa de ajo", "Crema acida",
    "Salsa de tomate", "Salsa chilena", "Pesto",
    # ACOMPANAMIENTOS
    "Arroz", "Pure", "Ensaladas", "Verduras asadas", "Papas fritas", "Papas gajo",
    "Papas salteadas", "Cus cus"
    # POSTRE
    "Suspiro Limeno", "Leche Asada", "Mousse de manjar", "Mousse de frutilla",
    "Panacota", "Flan", "Rosquillas"]


def generate_ingredients():
    ingredients = []
    for ingredient_data in INGREDIENTS:
        ingredient = Ingredient.objects.create(name=ingredient_data)
        ingredients.append(ingredient)
    return ingredients


def generate_plates(n=10, k=3, ingredients=[]):
    plates = []
    for p in range(n):
        ing = random.sample(ingredients, k)
        plate_name = "{} con {} y {}".format(
            ing[0].name, ing[1].name, ing[2].name
        )
        plate = Plate.objects.create(name=plate_name)
        plate.ingredients.set(ing)
        plate.save()
        plates.append(plate)
    return plates


def generate_menus(n=10, k=3, j=3, plates=[]):
    menus = []
    public_menus = []

    from datetime import date, timedelta, datetime
    today = date.today()

    # Generate one menu per day and publish it
    for days in range(n):
        for mn in range(j):
            plts = random.sample(plates, k)
            menu_date = today + timedelta(days=days)
            menu_date_str = datetime.strptime(
                menu_date, '%Y-%m-%d')
            menu_name = "Menu {} del {}".format(
                mn,
                menu_date_str
            )
            menu_code = f"M-{mn}-00{days}"
            menu = Menu.objects.create(
                name=menu_name,
                code=menu_code)
            menu.plates.set(plts)
            menu.save()
            menu.append(menu)

            public_menu = PublicMenu.objects.create(
                capacity=100,
                pub_date=menu_date_str,
                menu=menu.id
            )
            public_menus.append(public_menu)
    return menus, public_menus


def generate_user(n=5):
    users = []
    for u in range(n):
        user = RandomUser({'nat': 'es'})
        first_name = user.get_first_name()
        email = user.get_email()

        password = '12345678'

        user = User.objects.create_user(first_name.lower(), email, password)
        user.save()
        users.append(user)

    return users


def generate_schedule_menu(public_menus, users):
    scheduled_menus = []
    for public_menu in public_menus:
        # Select Plate of a menu
        menu = public_menu.menu
        plate = random.choices(population=menu.plates)[0]
        user = random.choices(population=users)[0]

        schedule_menu = ScheduleMenu.objects.create(
            pub_date=public_menu.pub_date,
            plate=plate.id,
            user=user.id
        )

        scheduled_menus.append(schedule_menu)


def main():
    users = generate_user()
    print("USUARIOS", users)
    ingredients = generate_ingredients()
    print("INGREDIENTES", ingredients)
    plates = generate_plates(ingredients=ingredients)
    print("PLATES", plates)
    menus, public_menus = generate_menus(plates=plates)
    print("MENUS", menus)
    print("PUBLIC MENUS", public_menus)
    scheduled_menus = generate_schedule_menu(public_menus, users)
    print("SCHEDULED MENUS", scheduled_menus)


if __name__ == "__main__":
    print("RUNNING SEEDS POPULATION")
    main()
