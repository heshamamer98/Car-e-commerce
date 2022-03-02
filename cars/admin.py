from operator import imod
from django.contrib import admin


from cars.models import Brand, Car, ImageCar, Order_item, Requests_Car



admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(ImageCar)
admin.site.register(Order_item)
admin.site.register(Requests_Car)