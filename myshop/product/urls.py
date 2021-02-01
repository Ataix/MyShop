from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoriesList, ProductViewSet, ReviewViewSet, WishViewSet

product_router = DefaultRouter()
product_router.register('', ProductViewSet)

review_router = DefaultRouter()
review_router.register('', ReviewViewSet)

wish_router = DefaultRouter()
wish_router.register('', WishViewSet)

urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path('', include(product_router.urls)),
    path('<str:short_title>/reviews/', include(review_router.urls)),
    path('<str:username>/wishlist/', include(wish_router.urls))
]