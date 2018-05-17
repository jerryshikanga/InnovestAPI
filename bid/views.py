from rest_framework import generics,permissions, views
from .models import Bid
from . serializers import BidSerializer, NewBidSerializer
from rest_framework.response import Response


# Create your views here.
class ListBid(generics.ListAPIView) :
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        if self.request.user.is_authenticated :
            return Bid.objects.filter(user=self.request.user)
        else :
            return Bid.objects.all()


class NewBid(views.APIView) :
    def post (self, request, format=None, **kwargs):
        serializer = NewBidSerializer(data=request.data)
        if serializer.is_valid() :
            if serializer.validated_data['amount'] < self.request.user.account.balance :
                if serializer.validated_data['amount'] <= 0 :
                    response = {
                        'status': False,
                        'message': "Invalid amount"
                    }
                    return Response(response)
                else :
                    bid = serializer.save(user=request.user)
                    response = {
                        'status':True,
                        'message':"Bid placed successfully"
                    }
                    return Response(response)
            else :
                return Response({
                    "status" : False,
                    "message":"Insufficient balance",
                    "amount":serializer.validated_data['amount'],
                    "balance": self.request.user.account.balance,
                })
        else :
            return Response(serializer.errors, status=400)
