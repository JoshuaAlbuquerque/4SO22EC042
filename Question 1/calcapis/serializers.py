# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import NumberStorage

# Create a model serializer
class CalculatorSerializer(serializers.HyperlinkedModelSerializer):
	# specify model and fields
	class Meta:
		model = NumberStorage
		fields = ('title', 'description')
