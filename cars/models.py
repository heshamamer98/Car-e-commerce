from PIL import Image
from django.db import models
from project.utils.models import Entity
from django.contrib.auth import get_user_model

User = get_user_model()


class Brand(Entity):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, verbose_name='users', related_name='brands', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name



class Car(Entity):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    mudel = models.IntegerField()
    transmission = models.CharField(max_length=100)
    engin_size = models.CharField(max_length=100)
    powerBHP = models.CharField(max_length=100)
    distance_meter = models.CharField(max_length=100)
    discription = models.TextField()
    price = models.FloatField()
    is_salled = models.BooleanField('is salled')
    user = models.ForeignKey(User, verbose_name='users', related_name='cars', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name='brands', related_name='cars', on_delete=models.CASCADE)
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)


    def __str__(self):
        return self.name


class CarColor(Entity):
    car = models.ForeignKey(Car, verbose_name='cars', related_name='colors',on_delete=models.CASCADE)
    color = models.CharField(max_length=7)
    quantity = models.IntegerField(default=0)


class BuyCar(Entity):
    user = models.ForeignKey(User, verbose_name='users', related_name='Buys', on_delete=models.CASCADE)
    car = models.ForeignKey(CarColor, verbose_name='CarColors', related_name='buys',on_delete=models.CASCADE)


class RequestCar(Entity):
    user = models.ForeignKey(User, verbose_name='users', related_name='Requests', on_delete=models.CASCADE)
    car = models.ForeignKey(CarColor, verbose_name='CarColors', related_name='carcolors',on_delete=models.CASCADE)



class ImageCar(Entity):
    image = models.ImageField('image', upload_to='car/')
    car = models.ForeignKey(Car, verbose_name='cars', related_name='images',on_delete=models.CASCADE)


    def __str__(self):
        return self.image.path


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)



class Order_item(Entity):
    user = models.ForeignKey(User, verbose_name='users', related_name='order_items', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, verbose_name='cars',
                                on_delete=models.CASCADE)
    total = models.DecimalField('total', blank=True, null=True, max_digits=1000, decimal_places=0)
    note = models.CharField('note', null=True, blank=True, max_length=100)
    ordered = models.BooleanField('ordered')


    def __str__(self):
        return self.car.name
