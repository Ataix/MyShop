from django.contrib.auth import get_user_model
from rest_framework import status, mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, AccountSerializer
from .utils import send_activation_email, IsOwnerAccount

ShopUser = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_email(user)
        return Response('Account created', status=status.HTTP_200_OK)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(ShopUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'activated',
            status=status.HTTP_200_OK
        )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            'Logout successful'
        )


class AccountViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = ShopUser.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerAccount]
    lookup_field = 'username'
