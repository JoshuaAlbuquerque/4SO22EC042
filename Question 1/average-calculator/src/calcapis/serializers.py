from rest_framework import serializers

class AverageCalculatorSerializer(serializers.Serializer):
    stored_numbers_before = serializers.ListField(child=serializers.FloatField())
    stored_numbers_after = serializers.ListField(child=serializers.FloatField())
    average = serializers.FloatField()