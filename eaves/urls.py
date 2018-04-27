# coding=utf-8
from django.urls import path
from eaves.views.Apartment import *

urlpatterns = [
    path('api/apt/', ApartmentListView.as_view()),
]
