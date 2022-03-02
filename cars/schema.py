from typing import List
from pydantic import UUID4
from ninja import ModelSchema, Schema
from django.contrib.auth.models import User


class UUIDSchema(Schema):
    id: UUID4


class UserOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username']
        # model_exclude = ['created', 'updated']            # else this fields



class BrandsOut(UUIDSchema):
    name : str



class AddBrands(Schema):
    name : str


class CarOut(UUIDSchema):
    name : str
    color: str
    status: str
    mudel: int
    transmission: str
    engin_size: str
    powerBHP: str
    distance_meter: str
    discription: str
    price: float
    is_salled: bool



class BrandsOutWithCars(UUIDSchema):
    name : str
    cars: List[CarOut]


class ImageCarOut(UUIDSchema):
    name : str


class ImageOut(UUIDSchema):
    image: str
    car: ImageCarOut


class OrderItemOut(UUIDSchema):
    user: UserOut
    car: ImageCarOut
    total: float
    note: str
    ordered: bool



# Home

class HomeImageCarOut(Schema):
    image: str


class HomeCarOut(UUIDSchema):
    name: str
    price: float
    images: List[HomeImageCarOut]


class HomeBrandsOut(UUIDSchema):
    name : str
    cars: List[HomeCarOut]


# One car

class OneCarOut(UUIDSchema):
    name : str
    color: str
    status: str
    mudel: int
    transmission: str
    engin_size: str
    powerBHP: str
    distance_meter: str
    discription: str
    price: float
    is_salled: bool
    images: List[HomeImageCarOut]



class NewSchema(Schema):
    one_car: OneCarOut
    new: List[HomeCarOut]



class PaginatedOneBrand(Schema):
    total_count: int
    per_page: int
    from_record: int
    to_record: int
    previous_page: int
    current_page: int
    next_page: int
    page_count: int
    data: List[HomeCarOut]


class recuest_color(Schema):
    user_color: str



class RequestCarOut(UUIDSchema):
    name : str
    color: str
    status: str
    mudel: int
    transmission: str
    engin_size: str
    powerBHP: str
    distance_meter: str