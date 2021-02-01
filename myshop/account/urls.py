from django.urls import path

from .views import RegisterView, ActivationView, LoginView, LogoutView, AccountViewSet

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/<str:username>/', AccountViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update'
    }))
]
