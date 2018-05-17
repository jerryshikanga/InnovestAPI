from .serializers import ReferalSerializer
from bid.models import Bid
from django.contrib.auth.models import User
from campaign.models import Campaign
from django.views import View
from django.db.models import Sum, Avg, Max, Min
from django.http import JsonResponse
from rest_framework.views import APIView


class StatisticsView(View):

    def get(self, request):
        bids = Bid.objects.aggregate(Sum('amount'), Avg('amount'), Max("amount"), Min("amount"))

        response = {
            'user_count': User.objects.count(),
            'campaign_count': Campaign.objects.count(),
            'bid_count': Bid.objects.count(),
            'bid_total': bids.get("amount__sum"),
            'bid_avg': bids.get("amount__avg"),
            'bid_min': bids.get("amount__min"),
            'bid_max': bids.get("amount__max"),
        }
        return JsonResponse(response)


class ReferUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReferalSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(request)
