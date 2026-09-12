from django.urls import path
from .views import get_car_price
from .views import TidioBookingWebhookView


urlpatterns = [
    path("car-price/", get_car_price),
    path('tidio-booking/', TidioBookingWebhookView.as_view(), name='tidio-booking'),
]