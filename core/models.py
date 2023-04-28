from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')


class CartProduct(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_constraint=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=False)
    address = models.CharField(max_length=200)
