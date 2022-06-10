from rest_framework import serializers
from .models import ReviewData
from .models import BuildingData

class BuildingSerializer(serializers.ModelSerializer) :
    class Meta :
        model = BuildingData        
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer) :
    class Meta :
        model = ReviewData        
        fields = '__all__'