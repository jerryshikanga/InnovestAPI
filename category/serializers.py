from .models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    campaigns = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'picture', 'description', 'summary', 'campaigns']
        read_only_fields = ['id', 'date']
