from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import  TawjihiSerlaizer, ReservationSerlaizer
from .models import Tawjihi, Reservation
# Create your views here.

class TawjihiViewSet(viewsets.ModelViewSet):
    queryset = Tawjihi
    serializer_class = TawjihiSerlaizer
    filter_backends = DjangoFilterBackend
    filterset_fields = ['course_categroy']

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerlaizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'tawgihi__category', 'contacted', 'field_of_Study', 'created_at']
    search_fields = ['name', 'phone_number']
