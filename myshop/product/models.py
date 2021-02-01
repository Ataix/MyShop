from time import time

from django.contrib.auth import get_user_model
from django.db import models

from pytils.translit import slugify

from account.models import ShopUser


def generate_slug(slug):
    sluging = slugify(slug)
    return sluging


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=50, unique=True, primary_key=True, blank=True)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = generate_slug(self.name)
        super().save()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    short_title = models.CharField(max_length=128, primary_key=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='categories')
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='product_author', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.short_title:
            slug_title = self.title[:15] + '-' + str(int(time()))
            self.short_title = slug_title
        super().save(*args, **kwargs)


class WishProduct(models.Model):
    customer = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='wish_user', blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wish_item')


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/img')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)


# class StarRating(models.Model):
#     star = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='star_product')


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)
    # star = models.ForeignKey(StarRating, related_name='star_rating', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}'s Review about {self.product} {self.pub_date} {self.text}"
