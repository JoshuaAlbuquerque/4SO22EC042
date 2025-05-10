from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .models import NumberStorage
from django.db import IntegrityError
import time

class AverageCalculatorViewSet(viewsets.ViewSet):
    window_size = 10

    @action(detail=True, methods=['get'], url_path='numbers/(?P<numberid>[^/.]+)')
    def get_numbers(self, request, numberid=None):
        if numberid not in ['p', 'f', 'e', 'r']:
            return Response({"error": "Invalid number ID."}, status=status.HTTP_400_BAD_REQUEST)

        start_time = time.time()
        url = f"https://third-party-server.com/api/numbers/{numberid}"
        try:
            response = requests.get(url, timeout=0.5)
            response.raise_for_status()
            fetched_numbers = response.json().get('numbers', [])
        except (requests.exceptions.RequestException, ValueError):
            return Response({"error": "Failed to fetch numbers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        unique_numbers = set()
        for number in fetched_numbers:
            try:
                unique_numbers.add(number)
                NumberStorage.objects.create(number=number)
            except IntegrityError:
                continue  # Ignore duplicates

        stored_numbers = list(NumberStorage.objects.values_list('number', flat=True).distinct())
        if len(stored_numbers) > self.window_size:
            stored_numbers = stored_numbers[-self.window_size:]

        average = sum(stored_numbers) / len(stored_numbers) if stored_numbers else 0

        return Response({
            "stored_before": stored_numbers,
            "stored_after": list(unique_numbers),
            "average": average
        }, status=status.HTTP_200_OK)