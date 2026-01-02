from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    WALLET_TYPES = (
        ('momo', 'Mobile Money'),
        ('card', 'Card'),
    )

    SCHEMES = (
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('mtn', 'MTN'),
        ('vodafone', 'Vodafone'),
        ('at', 'AT'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=WALLET_TYPES)
    account_number = models.CharField(max_length=6)  # first 6 digits only
    account_scheme = models.CharField(max_length=20, choices=SCHEMES)
    owner = models.CharField(max_length=20)  # phone number
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')

    class Meta:
        unique_together = ('user', 'account_number', 'account_scheme')

    def __str__(self):
        return f"{self.name} - {self.user.username}"
