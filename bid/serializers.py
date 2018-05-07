from rest_framework import serializers
from .models import Bid


class BidSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Bid
        fields = ['user', 'campaign', 'amount', 'date', 'id']
        read_only_fields = ['id', 'user']