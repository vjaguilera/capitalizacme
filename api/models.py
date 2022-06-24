from django.db import models

# Create your models here.


class Coyote(models.Model):
    # Name of the Coyote
    name = models.CharField(max_length=255, null=False)
    # Email of the Coyote
    email = models.EmailField(null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.email)


class Ingredient(models.Model):
    # Name of the menu
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{}".format(self.name)


class Plate(models.Model):
    # Name of the menu
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.personalized)

    # Menu Code
    personalized = models.BooleanField(default=False)

    # Ingredients of the plate
    ingredients = models.ManyToManyField(Ingredient)


class Menu(models.Model):
    # Name of the menu
    name = models.CharField(max_length=255, null=False)

    # Menu Code
    code = models.CharField(max_length=16, null=False)

    # Plates of a Menu
    plates = models.ManyToManyField(Plate)

    def __str__(self):
        return "{} - code: {}".format(self.name, self.code)


class PublicMenu(models.Model):
    capacity = models.IntegerField(default=100)
    pub_date = models.DateField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pub_date} - {self.menu.name}"

    class Meta:
        ordering = ['pub_date']


class ScheduleMenu(models.Model):
    pub_date = models.DateField()
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE)
    coyote = models.ForeignKey(Coyote, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pub_date} - {self.coyote.name} - {self.plate.name}"

    class Meta:
        ordering = ['pub_date']
