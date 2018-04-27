# coding=utf-8
from rest_framework import serializers
from eaves.models import *


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'
