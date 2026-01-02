from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

class Wallet(models.Model):
    TYPE_CHOICES = [
        ('momo', 'Momo'),
        ('card', 'Card'),
    ]
    SCHEME_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('mtn', 'MTN'),
        ('vodafone', 'Vodafone'),
        ('airteltigo', 'AirtelTigo'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    account_number = models.CharField(max_length=20)
    account_scheme = models.CharField(max_length=20, choices=SCHEME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
