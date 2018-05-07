from django.urls import path
from .import views

app_name = 'account'

urlpatterns = [
    path('api/', views.ListAccount.as_view(), name='list_create_account'),
    path('api/<int:id>/', views.RetrieveUpdateDestroyAccount.as_view(), name='retrieve_update_destroy-account'),
    path('user/', views.ListCreateUser.as_view(), name='list_create_user'),
    path('user/<int:pk>/', views.RetrieveUpdateDestroyUser.as_view(), name='user_api_view'),
    path('token/', views.CustomAuthToken.as_view(), name='obtain_token'),
]
