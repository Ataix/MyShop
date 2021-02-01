from rest_framework import permissions


class IsOwnerProduct(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return str(obj.username.username) == request.user.username or bool(request.user and request.user.is_superuser)


class IsOwnerReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return str(obj.author.username) == request.user.username or bool(request.user and request.user.is_superuser)


class IsOwnerWish(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return str(obj.customer.username) == request.user.username or bool(request.user and request.user.is_superuser)


class IsSellerAccount(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_seller) or bool(request.user and request.user.is_superuser)
