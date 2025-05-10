from django.contrib import admin
from .models import CalculatorTestModel, FetchedNumber

admin.site.register(CalculatorTestModel)
admin.site.register(FetchedNumber)