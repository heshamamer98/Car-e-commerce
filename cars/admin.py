from operator import imod
from django.contrib import admin


from cars.models import Brand, Car, ImageCar, Order_item, CarColor, RequestCar



admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(ImageCar)
admin.site.register(Order_item)
admin.site.register(CarColor)
admin.site.register(RequestCar)