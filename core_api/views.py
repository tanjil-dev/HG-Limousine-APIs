from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from .models import CarModel


@csrf_exempt
@api_view(["POST"])
def get_car_price(request):

    car_name = request.data.get("name")

    if not car_name:
        return Response(
            "Car name is required",
            status=400
        )

    try:
        car = CarModel.objects.get(
            name__iexact=car_name.strip()
        )

    except CarModel.DoesNotExist:
        return Response(
            "Car model not found",
            status=404
        )


    quote_message = (
        f"Vehicle: {car.name} | "
        f"Starting Price: ${car.base_price} | "
        f"Rate: ${car.per_km_rate}/mi"
    )


    return Response(quote_message)