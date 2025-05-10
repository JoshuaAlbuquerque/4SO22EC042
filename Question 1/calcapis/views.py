from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CalculatorSerializer
from .models import CalculatorTestModel
 
# create a viewset
 
class CalculatorViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = CalculatorTestModel.objects.all()
 
    # specify serializer to be used
    serializer_class = CalculatorSerializer