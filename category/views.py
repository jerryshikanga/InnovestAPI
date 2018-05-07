from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer
from .permissions import CategoryPermissions


# Create your views here.
class ListCreateCategory(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CategoryPermissions]


class RetrieveUpdateDestroyCategory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CategoryPermissions]