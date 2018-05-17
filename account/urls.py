from django.urls import path, include
from .import views

app_name = 'account'

urlpatterns = [
    path('api/', views.ListAccount.as_view(), name='list_create_account'),
    path('api/<int:pk>/', views.RetrieveUpdateDestroyAccount.as_view(), name='retrieve_update_destroy-account'),
    path('user/', views.ListCreateUser.as_view(), name='list_create_user'),
    path('user/<int:pk>/', views.RetrieveUpdateDestroyUser.as_view(), name='user_api_view'),
    path('token/', views.CustomAuthToken.as_view(), name='obtain_token'),
    path('deposit/request/', views.DepositRequest.as_view(), name='deposit_request'),
    path('withdraw/request/', views.WithdrawRequest.as_view(), name='withdraw_request'),
    path('password/change/', views.PasswordChange.as_view(), name='password_change'),
    path('password/reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('update/', views.UpdateAccount.as_view(), name='update_account'),

    path('mpesa/c2b/validation/', views.MpesaC2bValidation.as_view(), name='mpesa_c2b_validation'),
    path('mpesa/c2b/confirmation/', views.MpesaC2bConfirmation.as_view(), name='mpesa_c2b_confirmation'),
    path('mpesa/b2c/listener/', views.MpesaB2CListener.as_view(), name='mpesa_b2c_listener'),
]
