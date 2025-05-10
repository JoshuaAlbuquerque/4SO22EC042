from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AverageCalculatorViewSet

router = DefaultRouter()
router.register(r'average-calculator', AverageCalculatorViewSet, basename='average-calculator')

urlpatterns = [
    path('', include(router.urls)),
]