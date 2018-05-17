from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['name', 'start', 'end', 'summary', 'description', 'picture', 'category', 'user', 'id', 'amount']
        read_only_fields = ['user', 'id', 'start']
        write_only_fields =[]


class CampaignPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['picture']
