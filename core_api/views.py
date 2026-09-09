from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import CarModel


@csrf_exempt
@api_view(["POST"])
def get_car_price(request):

    car_name = request.data.get("name")


    if not car_name:
        return Response({
            "error": "name is required"
        }, status=400)


    try:
        car = CarModel.objects.get(
            name=car_name
        )

    except CarModel.DoesNotExist:

        return Response({
            "error": "Car model not found"
        }, status=404)


    return Response({

        "name": car.name,

        "base_price": f"${car.base_price}",

        "per_mi_rate": f"${car.per_km_rate}/mi"

    })