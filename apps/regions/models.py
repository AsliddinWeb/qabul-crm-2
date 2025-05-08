from django.db import models

class Country(models.Model):
    """Davlatlar (masalan: O‘zbekiston, Qozog‘iston, Rossiya)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    """Viloyat yoki shaharlar (masalan: Toshkent, Andijon, Qoraqalpog‘iston)"""
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class District(models.Model):
    """Tumanlar yoki shaharchalar, viloyatga bog‘langan"""
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('name', 'region')

    def __str__(self):
        return f"{self.name}, {self.region.name}"
