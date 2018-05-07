from rest_framework import generics, permissions, views, response
from .models import Campaign
from .serializers import CampaignSerializer, CampaignPictureSerializer
from .permissions import IsOwnerOrReadOnly


# Create your views here.
class ListCreateCampaign(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CampaignSerializer

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