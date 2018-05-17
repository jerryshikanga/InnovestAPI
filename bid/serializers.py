from rest_framework import serializers
from .models import Bid


class BidSerializer(serializers.ModelSerializer) :
    campaign = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta :
        model = Bid
        fields = ['user', 'campaign', 'amount', 'date', 'id']
        read_only_fields = ['id', 'user']


class NewBidSerializer(serializers.ModelSerializer):
    """docstring for NewBidSerializer."""
    class Meta :
        model = Bid
        fields = ['user', 'campaign', 'amount', 'date', 'id']
        read_only_fields = ['id', 'user']
