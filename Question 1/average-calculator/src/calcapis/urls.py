from django.urls import path
from .views import AverageCalculatorView

urlpatterns = [
    path('numbers/<str:numberid>/', AverageCalculatorView.as_view(), name='average_calculator'),
]