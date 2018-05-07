from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('api/', views.ListCreateCategory.as_view(), name='list_create_category'),
    path('api/<int:pk>', views.RetrieveUpdateDestroyCategory.as_view(), name='retrieve_update_destroy_category'),
]
