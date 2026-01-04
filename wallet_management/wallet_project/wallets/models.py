from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    objects = models.Manager()
    WALLET_TYPES = [
        ('momo', 'Mobile Money'),
        ('card', 'Card'),
    ]

    SCHEMES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('mtn', 'MTN'),
        ('telecel', 'Telecel'),
        ('at', 'AT'),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=WALLET_TYPES)
    account_number = models.CharField(max_length=6)  # truncated
    account_scheme = models.CharField(max_length=20, choices=SCHEMES)
    owner = models.CharField(max_length=15)  # phone number
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'account_number', 'account_scheme'],
                name='unique_wallet_per_user'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.account_scheme})"
