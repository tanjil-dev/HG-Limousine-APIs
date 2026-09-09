from django.urls import path
from .views import get_car_price


urlpatterns = [
    path(
        "car-price/",
        get_car_price
    ),
]