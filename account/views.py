from rest_framework import status, generics, permissions, parsers
from .models import Account
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import AccountSerializer, UserSerializer, PasswordChangeSerializer, PasswordResetSerializer, AccountUpdateSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import pympesa
import datetime
import base64
from django.conf import settings
import json
from django.contrib.auth import  update_session_auth_hash
from .serializers import MpesaC2BValidationSerializer, MpesaC2bConfirmationSerializer, MpesaB2CListnerSerializer, WithdrawRequestSerializer, DepositRequestSerializer


# Create your views here.
class ListAccount(generics.ListAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = AccountSerializer


class RetrieveUpdateDestroyAccount(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = AccountSerializer


class RetrieveUpdateDestroyUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]


class ListCreateUser(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            "user": {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
            },
            
        })


class DepositRequest(APIView):

    def post(self, request, format=None, *args, **kwargs):

        serializer = DepositRequestSerializer(data=request.data)

        if serializer.is_valid():

            access_token = pympesa.oauth_generate_token(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET,
                                                        grant_type="client_credentials",
                                                        env=settings.MPESA_ENVIRONMENT).json().get("access_token")
            mpesa_client = pympesa.Pympesa(access_token, env=settings.MPESA_ENVIRONMENT)

            if request.data.get("phone_number")  is not None :
                phone_number = request.data.get("phone_number")
            else :
                phone_number = request.user.account.telephone
            amount = serializer.data.get("amount")
            account_ref = request.user.username

            account_desc = "Deposit"
            timenow = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
            data = settings.LIPA_NA_MPESA_ONLINE_SHORTCODE + settings.LIPA_NA_MPESA_ONLINE_PASSKEY + timenow
            data_bytes = data.encode("utf-8")
            password_bytes = base64.b64encode(data_bytes)
            password = password_bytes.decode("utf-8")
            resp = mpesa_client.lipa_na_mpesa_online_payment(
                BusinessShortCode=settings.LIPA_NA_MPESA_ONLINE_SHORTCODE,
                Password=password,
                Timestamp=timenow,
                TransactionType="CustomerPayBillOnline",
                Amount=amount,
                PartyA=phone_number,
                PartyB=settings.LIPA_NA_MPESA_ONLINE_SHORTCODE,
                PhoneNumber=phone_number,
                CallBackURL="http://shikanga.pythonanaywhere.com",
                AccountReference=account_ref,
                TransactionDesc=account_desc
            )
            response = json.loads(resp.content.decode("utf-8"))
            # expected response payload
            # [
            # "MerchantRequestID",
            # "CheckoutRequestID",
            # "ResponseCode",
            # "ResponseDescription",
            # "CustomerMessage"
            # ]
            status = False
            api_response = dict()
            if "MerchantRequestID" in response and "CheckoutRequestID" in response:
                status = True
            if status:
                api_response = {
                    "status": status,
                    "ResponseDescription": response.get("ResponseDescription"),
                    "CustomerMessage": response.get("CustomerMessage"),
                }
            return Response(api_response)
        else :
            return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawRequest(APIView) :

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = WithdrawRequestSerializer(data=request.data)
        if serializer.is_valid() :
            access_token = pympesa.oauth_generate_token(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET,
                                                        grant_type="client_credentials",
                                                        env=settings.MPESA_ENVIRONMENT).json().get("access_token")
            mpesa_client = pympesa.Pympesa(access_token, env=settings.MPESA_ENVIRONMENT)
            if request.data.get("phone_number")  is not None :
                phone_number = request.data.get("phone_number")
            else :
                phone_number = request.user.account.telephone
            resp = mpesa_client.b2c_payment_request(
                InitiatorName=settings.MPESA_INITIATOR_NAME_SC_1,
                SecurityCredential=settings.MPESA_SECURITY_CREDENTIAL_SC_1,
                CommandID="BusinessPayment",
                Amount=serializer.data['amount'],
                PartyA=settings.MPESA_SHORTCODE_1,
                PartyB=phone_number,
                Remarks="Withdrawal "+user.username,
                QueueTimeOutURL="http://shikanga.pythonanywhere.com/account/api/",
                ResultURL="http://shikanga.pythonanywhere.com/account/api/",
                Occassion="Withdrawal"
            )
            response = json.loads(resp.content.decode("utf-8"))
            # expected response
            # {
            #     "ConversationID": "AG_20180514_0000748958ffe87dfaed",
            #     "OriginatorConversationID": "16927-1492048-1",
            #     "ResponseCode": "0",
            #     "ResponseDescription": "Accept the service request successfully."
            # }
            status = False
            if "ConversationID" in response and "OriginatorConversationID" in response :
                status =True

            if status :
                api_response = {
                    "status" : status,
                    "ResponseDescription" : response.get("ResponseDescription"),
                    "ResponseCode" : response.get("ResponseCode"),
                }
            else :
                api_response = {
                    "status" : status,
                }
            if status:
                code = status.HTTP_202_ACCEPTED
            else :
                code = status.HTTP_400_BAD_REQUEST
            return  Response(api_response, status=code)
        else :
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not self.request.user.check_password(serializer.data.get('old_password')):
                response = {
                    'status':False,
                    'old_password': ['Wrong old password']
                }
                return Response (response, status=status.HTTP_400_BAD_REQUEST )
            self.request.user.set_password(serializer.data.get('new_password'))
            self.request.user.save()
            update_session_auth_hash(request=self.request, user=self.request.user)
            response = {
                'status':True,
                'message':'Password Reset',
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MpesaC2bValidation(APIView) :
    parser_classes = [parsers.JSONParser, ]
    permission_classes =  [permissions.AllowAny, ]
    """return "ResultCode"= > 0 meaning your accept the transaction and "ResultCode" = > 1,"""
    def post(self, request, *args, **kwargs):
        serializer = MpesaC2BValidationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['BillRefNumber']

            try :
                user = User.objects.get(username=username)
                response = {
                    'ResultCode': 0,
                    'ResultDesc': 'Service processing successful'
                }
                return Response(response, status=200)
            except :
                response = {
                    'ResultCode': 1,
                    'ResultDesc': 'Invalid user'
                }
                return Response(response, status=400)

        response = {
            'ResultCode' : 1,
            'ResultDesc' : 'Invalid payload',
        }
        response = {**response, **serializer.errors}
        return Response(response, status=400)


class MpesaC2bConfirmation(APIView) :
    permission_classes = [permissions.AllowAny, ]
    parser_classes = [parsers.JSONParser, ]

    def post(self, request, *args, **kwargs):
        serializer = MpesaC2bConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'ResultCode': 0,
                'ResultDesc': 'Service processing successful'
            }
            return Response(response, status=200)
        response = {
            'ResultCode' : 1,
            'ResultDesc' : 'Invalid payload',
        }
        response = {**response, **serializer.errors}
        return Response(response, status=400)

class MpesaB2CListener(APIView) :
    permission_classes =  [permissions.AllowAny, ]
    parser_classes =  [parsers.JSONParser, ]

    def post(self, request, *args, **kwargs):
        serializer = MpesaB2CListnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'ResultCode': 0,
                'ResultDesc': 'Service processing successful'
            }
            return Response(response, status=200)
        response = {
            'ResultCode' : 1,
            'ResultDesc' : 'Invalid payload',
        }
        response = {**response, **serializer.errors}
        return Response(response, status=400)


class PasswordReset(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAccount(APIView) :
    def post(self, request, *args, **kwargs):
        serializer = AccountUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            account = user.account
            user.first_name = serializer.validated_data.get("first_name")
            user.last_name = serializer.validated_data.get("last_name")
            account.picture = serializer.validated_data.get("picture")
            account.telephone = serializer.validated_data.get("telephone")
            user.save()
            account.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)