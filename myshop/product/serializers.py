from rest_framework import serializers

from .models import Category, Product, Review, WishProduct
from account.serializers import AccountSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishProduct
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['customer'] = instance.customer.username
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        customer = request.user
        validated_data['customer'] = customer
        wishproduct = WishProduct.objects.create(**validated_data)
        return wishproduct


class ReviewSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Review
        # exclude = ('author', )
        fields = "__all__"
    #
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     username = request.user
    #     validated_data['username'] = username
    #     review = Review.objects.create(**validated_data)
    #     return review

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['username'] = self.context.get('request').user.username
        # representation['username'] = AccountSerializer(data=instance.author).data
        return representation


class ProductImageMixin:
    def _get_img_url(self, obj):
        request = self.context.get('request')
        img_obj = obj.images.first()
        if img_obj is not None and img_obj.image:
            url = img_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''


class ProductSerializer(ProductImageMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_img_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['username'] = instance.username.username
        return representation


class ProductListSerializer(ProductImageMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('description', 'username')

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_img_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        return representation


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('description', )

    def create(self, validated_data):
        request = self.context.get('request')
        categories = validated_data.pop('categories')
        username = request.user
        validated_data['username'] = username
        product = Product.objects.create(**validated_data)
        for category in categories:
            product.categories.add(category)
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = self.context.get('request').user.username
        return representation
