from django.db import models
from django.db.models.base import Model
from django.urls import reverse

# Create your models here.
WASH = (
    ('1', 'Basic Wash'),
    ('2', 'Wash & vacuuming'),
    ('3', 'Wash & full Detailing')
)


class Accessory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={"car_id": self.id})


class Car(models.Model):
    nickname = models.CharField(max_length=40, default="no nickname")
    make = models.CharField(max_length=20, default="NA")
    model = models.CharField(max_length=20, default="NA")
    year = models.IntegerField(default=0)
    color = models.CharField(max_length=20, default="NA")
    description = models.CharField(max_length=50, default="NA")
    accessories = models.ManyToManyField(Accessory)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})


class Washing(models.Model):
    date = models.DateField('washing Date')
    intensity = models.CharField(
        max_length=1, choices=WASH, default=WASH[0][0])
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_intensity_display()} on {self.date}"

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id: {self.car_id} @{self.url}"
