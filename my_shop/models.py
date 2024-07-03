from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True, blank=True)
    on_sale = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return round(self.price * (1 - self.discount / 100), 2)
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-1'
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    body = models.TextField()
    is_possible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name
