from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


ShopUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    class Meta:
        model = ShopUser
        fields = (
            'password', 'password_confirm',
            'email', 'username', 'name', 'is_want_be_seller'
        )

    def validate_username(self, value):
        if ShopUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('username busy')
        return value

    def validate_email(self, value):
        if ShopUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('email busy')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('passwords does not same')
        return attrs

    def save(self, **kwargs):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        name = self.validated_data.get('name')
        is_want_be_seller = self.validated_data.get('is_want_be_seller')
        user = ShopUser.objects.create_user(
            username, email, password, is_want_be_seller=is_want_be_seller, name=name
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    'Can not login',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Write username password'
            )
        attrs['user'] = user
        return attrs


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ('username', 'name')
