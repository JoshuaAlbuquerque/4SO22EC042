from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .models import NumberStorage
from django.db import IntegrityError
import time

class AverageCalculatorViewSet(viewsets.ViewSet):
    window_size = 10

    API_URLS = {
        'p': 'http://20.244.56.144/evaluation-service/primes',
        'f': 'http://20.244.56.144/evaluation-service/fibo',
        'e': 'http://20.244.56.144/evaluation-service/even',
        'r': 'http://20.244.56.144/evaluation-service/rand',
    }

    auth_token = None
    token_expiry = 0

    def get_auth_token(self):
        print(f"Current UNIX time: {time.time()}")

        if self.auth_token and time.time() < self.token_expiry:
            return self.auth_token

        auth_url = "http://20.244.56.144/evaluation-service/auth"
        payload = {
            "email": "22f43.joshua@sjec.ac.in",
            "name": "joshua quinthino albuquerque",
            "rollNo": "4so22ec042",
            "accessCode": "KjJAxP",
            "clientID": "a376038d-b651-46e9-988f-ebdbffe52134",
            "clientSecret": "RSZBtNjQFYDmfTVR"
        }
        print(f"Auth token: {payload}")
        try:
            response = requests.post(auth_url, json=payload, timeout=5)
            response.raise_for_status()
            data = response.json()

            self.auth_token = data.get("access_token")
            expires_in = data.get("expires_in", 0)  
            if expires_in > 1000000000:  
                self.token_expiry = expires_in
            else: 
                self.token_expiry = time.time() + expires_in

            print(f"New auth token fetched successfully: {self.auth_token}")
            return self.auth_token
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Failed to fetch auth token: {e}")
            return None
    

    @action(detail=False, methods=['get'], url_path='numbers/(?P<numberid>[^/.]+)')
    def get_numbers(self, request, numberid=None):

        if numberid not in self.API_URLS:
            print(f"Invalid number ID: {numberid}")
            return Response({"error": "Invalid number ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the authorization token
        token = self.get_auth_token()
        if not token:
            print("Failed to obtain authorization token.")
            return Response({"error": "Failed to obtain authorization token."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = self.API_URLS[numberid]
        headers = {"Authorization": f"Bearer {token}"}
        print(f"Fetching numbers from API: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=0.5)
            response.raise_for_status()
            fetched_numbers = response.json().get('numbers', [])
            print(f"Numbers fetched successfully: {fetched_numbers}")
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Failed to fetch numbers from API: {e}")
            return Response({"error": "Failed to fetch numbers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        stored_before = list(NumberStorage.objects.values_list('number', flat=True).order_by('created_at'))
        print(f"Stored numbers before update: {stored_before}")
        for number in fetched_numbers:
            try:
                NumberStorage.objects.create(number=number)
            except IntegrityError:
                continue  # Ignore duplicates

        stored_after = list(NumberStorage.objects.values_list('number', flat=True).order_by('created_at'))
        if len(stored_after) > self.window_size:
            excess_count = len(stored_after) - self.window_size

            excess_objects = NumberStorage.objects.order_by('created_at')[:excess_count]
            for obj in excess_objects:
                obj.delete()
            stored_after = list(NumberStorage.objects.values_list('number', flat=True).order_by('created_at'))
        print(f"Stored numbers after update: {stored_after}")

        average = sum(stored_after) / len(stored_after) if stored_after else 0
        print(f"Calculated average: {average}")

        return Response({
            "stored_before": stored_before,
            "stored_after": stored_after,
            "average": average
        }, status=status.HTTP_200_OK)