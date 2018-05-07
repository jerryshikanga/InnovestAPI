from django.urls import path
from . import views

app_name = 'campaign'

urlpatterns = [
    path('api/', views.ListCreateCampaign.as_view(), name='list_create_campaign'),
    path('api/<int:pk>/', views.RetrieveUpdateDeleteCampaign.as_view(), name='retrieve_update_destroy_campaign'),
    path('picture/<int:pk>/', views.CampaignPicture.as_view(), name='update_campaign_picture'),
]
