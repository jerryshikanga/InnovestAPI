from rest_framework import generics, permissions, views, response
from .models import Campaign
from .serializers import CampaignSerializer, CampaignPictureSerializer
from .permissions import IsOwnerOrReadOnly
from category.models import Category
from django.shortcuts import get_object_or_404


# Create your views here.
class ListCreateCampaign(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CampaignSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListUserCampaigns(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CampaignSerializer

    def get_queryset(self):
        return Campaign.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDeleteCampaign(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CampaignSerializer


class CampaignPicture(generics.RetrieveUpdateAPIView) :
    queryset = Campaign.objects.all()
    serializer_class = CampaignPictureSerializer

    def perform_update(self, serializer):
        serializer.save(picture=self.request.FILES['picture'])


class ListCategoryCampaign(generics.ListAPIView) :
    serializer_class = CampaignSerializer
    permission_classes =  [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return Campaign.objects.filter(category=category)