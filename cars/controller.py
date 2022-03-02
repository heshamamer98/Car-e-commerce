from math import ceil
from turtle import color
from typing import List
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from pydantic import UUID4
from ninja import Router
from cars.schema import HomeBrandsOut, BrandsOut, CarOut, ImageOut, OrderItemOut,\
                        AddBrands, BrandsOutWithCars, NewSchema, HomeCarOut,\
                        PaginatedOneBrand, recuest_color, RequestCarOut
from project.utils.schemas import MessageOut
from cars.models import Brand, Car, Image, Order_item, Requests_Car
from account.authorization import GlobalAuth




pub_controller = Router()
cars_controller = Router()
home_controller = Router()


User = get_user_model()


@pub_controller.get('list_brands', response={
        200:List[BrandsOutWithCars],
        404: MessageOut
    })
def list_brands(request):

    brands = Brand.objects.all()
    if brands:
        return brands
    else:
        return 404, {'detail': 'No brands yet'}



@cars_controller.get('list_cars', response={
        200:List[CarOut],
        404: MessageOut
    })
def list_cars(request):
    
    cars = Car.objects.all()
    if cars:
        return cars
    else:
        return 404, {'detail': 'No cars yet'}
    


@pub_controller.get('list_images', response={
        200:List[ImageOut],
        404: MessageOut
    })
def list_images(request):
    
    images = Image.objects.all()
    if images:
        return images
    else:
        return 404, {'detail': 'No images yet'}


@pub_controller.get('list_OrderItem', response={
        200:List[OrderItemOut],
        404: MessageOut
    })
def list_images(request):

    Ordered_items = Order_item.objects.all()
    if Ordered_items:
        return Ordered_items
    else:
        return 404, {'detail': 'No Ordered items yet'}



@pub_controller.post('addBrand', auth=GlobalAuth(), response={
        201: BrandsOut,
        400: MessageOut
    })
def create_brand(request, brand_in: AddBrands):
    brand = Brand(**brand_in.dict(), user=get_object_or_404(User, id=request.auth['pk']))
    is_saved = brand.save()
    if is_saved:
        return 400, {'detail': 'Brand not saved'}
    else:
        return 201, brand
    

# Home

@home_controller.get('', response={
        200:List[HomeBrandsOut],
        404: MessageOut
    })
def home(request):

    brands = Brand.objects.all()
    if brands:
        return brands
    else:
        return 404, {'detail': 'No brands yet'}



# One car

# 312a14ca-9561-4dd3-8d10-904775c134af          id for test

@cars_controller.get('{id}', response={
    200: NewSchema,
    404: MessageOut
})
def retrieve_car(request, id: UUID4):
    one_car = get_object_or_404(Car, id=id)
    new = list(Car.objects.all())

    return {
        'one_car': one_car,
        'new': new,
    }



def paginated_response(queryset, *, per_page=10, page=1):
    try:
        total_count = len(queryset)
    except TypeError:
        total_count = 1
    limit = per_page
    offset = per_page * (page - 1)
    page_count = ceil(total_count / per_page)

    try:
        data = list(queryset[offset: limit + offset])
    except TypeError:
        data = queryset

    return {
        'total_count': total_count,
        'per_page': limit,
        'from_record': offset + 1,
        'to_record': (offset + limit) if (offset + limit) <= total_count else (total_count % per_page) + offset,
        'previous_page': page - 1 if page > 2 else 1,
        'current_page': page,
        'next_page': min(page + 1, page_count),
        'page_count': page_count,
        'data': data,
    }


def response(status, data, *, paginated: bool = False, per_page: int = 10, page: int = 1):
    if paginated:
        return status, paginated_response(data, per_page=per_page, page=page)

    return status, data


# http://127.0.0.1:8000/api/cars/list_brand_cars/BMW/2
# http://127.0.0.1:8000/api/cars/list_brand_cars/Audi/1
@cars_controller.get('list_brand_cars/{brand}/{page}', response={
        200: PaginatedOneBrand,
        404: MessageOut
    })
def list_brand_cars(request, brand: str, page: int):
    cars = Car.objects.filter(brand__name=brand)
    
    return response(200, cars, paginated=True, per_page=12, page=page)


@cars_controller.get('', response={
    200: List[HomeCarOut],
    404: MessageOut
})
def search_cars(
        request, *,
        name: str = None,
        color: str = None,
):

    if name and color:
        cars = Car.objects.filter(name=name, color=color)
        return cars

    else:
        cars = Car.objects.all()
        if cars:
            return cars
        else:
            return 404, {'detail': 'No products found'}



@cars_controller.get('add_fav/<id>', auth=GlobalAuth())
def add_fav(request, id):
    car = get_object_or_404(Car, id=id)
    if car.favourites.filter(id=request.auth['pk']).exists():
        car.favourites.remove(request.auth['pk'])
        return {
            'msg': 'removed from favourits'
        }
    else:
        car.favourites.add(request.auth['pk'])

        return {
            'msg': 'added to favourits'
        }


@pub_controller.get('list_fav', auth=GlobalAuth(), response={
        200: List[HomeCarOut],
        404: MessageOut
    })
def list_fav(request):
    cars = Car.objects.filter(favourites=request.auth['pk'])

    if cars:
        return cars
    else:
        return 404, {'detail': 'No favourites yet'}
        

@cars_controller.get('add_fav/<id>/req', auth=GlobalAuth(), response={
        201: RequestCarOut,
        400: MessageOut
    })
def request_car(request, id, recuest_color: recuest_color):
    car = get_object_or_404(Car, id=id)
    request_car = Requests_Car.objects.create(name=car.name, color=recuest_color, status=car.status, mudel=car.mudel, transmission=car.transmission, engin_size=car.engin_size, powerBHP=car.powerBHP, distance_meter=car.distance_meter, user=get_object_or_404(User, id=request.auth['pk']))
    if request_car:
        return 201, request_car
    else:
        return 400, {'detail': 'Request failed'}