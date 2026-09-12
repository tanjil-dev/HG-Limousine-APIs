from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .serializers import TidioBookingSerializer

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


class TidioBookingWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # Verify API Key from Tidio Header
        api_key = request.headers.get('X-API-KEY') or request.headers.get('Authorization')

        # If using Bearer format, clean up "Bearer " prefix if present
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key.replace('Bearer ', '')

        if not api_key or api_key != settings.TIDIO_API_KEY:
            return Response(
                "Unauthorized: Invalid or missing API Key.",
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = TidioBookingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        service_type = data.get('service_type')
        pickup = data.get('pickup_location')
        dropoff = data.get('dropoff_location')
        date = data.get('date')
        time = data.get('pickup_time')
        passengers = data.get('passengers')
        vehicle = data.get('vehicle_preference', 'N/A')
        name = data.get('name')
        phone = data.get('phone_number')
        customer_email = data.get('email')

        # 1. Email to Customer
        customer_subject = f"Your Ride Request Confirmation - {service_type}"
        customer_message = (
            f"Hello {name},\n\n"
            f"Thank you for reaching out! We have received your booking request details:\n\n"
            f"• Service Type: {service_type}\n"
            f"• Pickup Location: {pickup}\n"
            f"• Drop-off Location: {dropoff}\n"
            f"• Date: {date}\n"
            f"• Pickup Time: {time}\n"
            f"• Passengers: {passengers}\n"
            f"• Vehicle Preference: {vehicle}\n\n"
            f"Our team is reviewing your request and will follow up with you shortly at {phone}.\n\n"
            f"Best regards,\nBooking Team"
        )

        try:
            send_mail(
                subject=customer_subject,
                message=customer_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                f"Failed to send email to customer: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 2. Email to Admin
        admin_subject = f"New Booking Request ({service_type}) - {name}"
        admin_message = (
            f"New booking details submitted via Tidio Chat:\n\n"
            f"Customer Name: {name}\n"
            f"Email: {customer_email}\n"
            f"Phone: {phone}\n\n"
            f"--- Service Details ---\n"
            f"Service Type: {service_type}\n"
            f"Pickup Location: {pickup}\n"
            f"Drop-off Location: {dropoff}\n"
            f"Date: {date}\n"
            f"Time: {time}\n"
            f"Passengers: {passengers}\n"
            f"Vehicle Preference: {vehicle}\n"
        )

        try:
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                f"Failed to send email to admin: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            f"Booking request received and confirmation email sent to {customer_email}. Soon our team will contact you via {phone}.",
            status=status.HTTP_200_OK
        )