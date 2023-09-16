from rest_framework import serializers
from .models import Tawjihi, Reservation


class TawjihiSerlaizer(serializers.ModelSerializer):
    class Meta:
        model = Tawjihi
        fields = "__all__"


class ReservationSerlaizer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


