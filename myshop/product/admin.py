from django.contrib import admin

from .models import Category, Product, ProductImage, Review, WishProduct


class ImgInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image']


class ProductFull(admin.ModelAdmin):
    inlines = [
        ImgInline
    ]


admin.site.register(Category)
admin.site.register(Product, ProductFull)
admin.site.register(Review)
admin.site.register(WishProduct)
