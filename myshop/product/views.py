from django.db import models
from django.db.models import Q
from rest_framework import viewsets, status, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Category, Product, Review, WishProduct
from .serializers import CategorySerializer, ProductSerializer, \
    ProductListSerializer, ProductCreateUpdateSerializer, ReviewSerializer, WishSerializer
from .utils import IsSellerAccount, IsOwnerProduct, IsOwnerReview, IsOwnerWish


class ShopPagination(PageNumberPagination):
    page_size = 2


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ShopPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductSerializer
        elif self.action == 'list':
            return ProductListSerializer
        return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsOwnerProduct]
        elif self.action == 'create':
            permissions = [IsSellerAccount]
        else:
            permissions = []
        return [permission() for permission in permissions]

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) |
                                       Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet
                ):
    queryset = WishProduct.objects.all()
    permission_classes = [IsOwnerWish]
    serializer_class = WishSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user.id
        queryset = WishProduct.objects.filter(customer=user)
        serializer = WishSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        permissions = [IsOwnerWish]
        if self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsOwnerWish]
        return [permission() for permission in permissions]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        permissions = []
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsOwnerReview]
        return [permission() for permission in permissions]

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(text__icontains=q)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
