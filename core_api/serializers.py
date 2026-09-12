from rest_framework import serializers

class TidioBookingSerializer(serializers.Serializer):
    service_type = serializers.CharField(max_length=100)
    pickup_location = serializers.CharField(max_length=255)
    dropoff_location = serializers.CharField(max_length=255)
    date = serializers.CharField(max_length=50)
    pickup_time = serializers.CharField(max_length=50)
    passengers = serializers.CharField(max_length=50)
    vehicle_preference = serializers.CharField(max_length=100, required=False, allow_blank=True)
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=50)
    email = serializers.EmailField()