import random
from randomuser import RandomUser
import os
import django
import sys


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


def generate_ingredients(Ingredient):
    ingredients = []
    for ingredient_data in INGREDIENTS:
        ingredient = Ingredient.objects.create(name=ingredient_data)
        ingredients.append(ingredient)
    return ingredients


def generate_plates(Plate, n=10, k=3, ingredients=[]):
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


def generate_menus(Menu, PublicMenu, n=10, k=3, j=3, plates=[]):
    menus = []
    public_menus = []

    from datetime import date, timedelta, datetime
    today = date.today()

    # Generate one menu per day and publish it
    for days in range(n):
        for mn in range(j):
            plts = random.sample(plates, k)
            menu_date = today + timedelta(days=days)
            menu_date_str = menu_date.strftime('%Y-%m-%d')
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
            menus.append(menu)

            public_menu = PublicMenu.objects.create(
                capacity=100,
                pub_date=menu_date_str,
                menu=menu
            )
            public_menus.append(public_menu)
    return menus, public_menus


def generate_user(User, n=5):
    users = []
    for u in range(n):
        user = RandomUser({'nat': 'es'})
        first_name = user.get_first_name()
        first_name += str(u)
        email = user.get_email()

        password = '12345678'

        user = User.objects.create_user(first_name.lower(), email, password)
        user.save()
        users.append(user)

    return users


def generate_schedule_menu(ScheduleMenu, public_menus, users):
    scheduled_menus = []
    for public_menu in public_menus:
        # Select Plate of a menu
        menu = public_menu.menu
        plates = menu.plates.all()
        plate = plates[0]
        user = users[0]

        schedule_menu = ScheduleMenu.objects.create(
            pub_date=public_menu.pub_date,
            plate=plate,
            user=user
        )

        scheduled_menus.append(schedule_menu)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acme.settings")
    django.setup()

    from django.contrib.auth.models import User

    from api.models import (  # noqa: E402
        Ingredient,
        Plate,
        Menu,
        PublicMenu,
        ScheduleMenu,
    )

    users = generate_user(User=User)
    print("USUARIOS", users)
    ingredients = generate_ingredients(Ingredient=Ingredient)
    print("INGREDIENTES", ingredients)
    plates = generate_plates(Plate=Plate, ingredients=ingredients)
    print("PLATES", plates)
    menus, public_menus = generate_menus(
        Menu=Menu, PublicMenu=PublicMenu, plates=plates)
    print("MENUS", menus)
    print("PUBLIC MENUS", public_menus)
    scheduled_menus = generate_schedule_menu(
        ScheduleMenu=ScheduleMenu, public_menus=public_menus, users=users)
    print("SCHEDULED MENUS", scheduled_menus)


if __name__ == "__main__":
    print("RUNNING SEEDS POPULATION")
    main()
