from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    bids = serializers.StringRelatedField(many=True)


    class Meta:
        model = Campaign
        fields = ['name', 'start', 'end', 'summary', 'description', 'picture', 'category', 'user', 'id', 'bids']
        read_only_fields = ['user', 'id']
        write_only_fields =[]


class CampaignPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['picture']
