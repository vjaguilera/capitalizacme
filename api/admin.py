from django.contrib import admin
from .models import (
    Coyote,
    Ingredient,
    Plate,
    Menu,
    PublicMenu,
    ScheduleMenu
)
# Register your models here.
admin.site.register(Coyote)
admin.site.register(Ingredient)
admin.site.register(Plate)
admin.site.register(Menu)
admin.site.register(PublicMenu)
admin.site.register(ScheduleMenu)
