from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class ExteriorColor(models.Model):
    color = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.color


class Transmission(models.Model):
    transmission_type = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.transmission_type


class Car(models.Model):
    title = models.CharField(max_length=120)
    price = models.IntegerField()
    img_url = models.URLField(max_length=300) 
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    year = models.IntegerField()
    extcolor = models.ForeignKey(ExteriorColor, on_delete=models.CASCADE)
    trans = models.ForeignKey(Transmission, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'img_url')



