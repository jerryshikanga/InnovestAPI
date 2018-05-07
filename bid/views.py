from rest_framework import generics,permissions, views, response
from .models import Bid
from . serializers import BidSerializer


# Create your views here.
class ListBid(generics.ListAPIView) :
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        if serializer.validated_data.get('amount') < self.request.user.account.balance :
            serializer.save(user=self.request.user)
        else :

            # return response({
            #     "error": "Account balance insufficient",
            #     "amount": serializer.validated_data.get('amount'),
            #     "balance": self.request.user.account.balance,
            # })
            pass

    def get_queryset(self):
        if self.request.user.is_authenticated :
            return Bid.objects.filter(user=self.request.user)
        else :
            return Bid.objects.all()


class NewBid(views.APIView) :
    def post (self, request, format=None, **kwargs):
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid() :
            if serializer.validated_data['amount'] < self.request.user.account.balance :
                bid = serializer.save()
                return response.Response(bid)
            else :
                return response.Response({
                    "error":"Insufficient balance",
                    "amount":serializer.validated_data['amount'],
                    "balance": self.request.user.account.balance,
                })