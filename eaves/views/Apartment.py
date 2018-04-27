# coding=utf-8
from django.shortcuts import render
from eaves.models import Apartment
from eaves.serializers import ApartmentSerializer
from rest_framework import generics


class ApartmentListCreate(generics.ListCreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class ApartmentListView(generics.ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
