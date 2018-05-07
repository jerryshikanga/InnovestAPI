from .import views
from  django.urls import  path

app_name = 'bid'

urlpatterns = [
    path('api/', views.ListBid.as_view(), name='list_create_bid'),
    path('new/', views.NewBid.as_view(), name='new_bid'),
]