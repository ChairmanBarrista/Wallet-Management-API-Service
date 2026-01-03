from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Wallet(models.Model):
    WALLET_TYPE_CHOICES = [
        ('momo', 'Mobile Money'),
        ('card', 'Card'),
    ]
  
    SCHEME_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('mtn', 'MTN'),
        ('vodafone', 'Vodafone'),
        ('airteltigo', 'AirtelTigo'),
    ]
    
    MOMO_SCHEMES = ['mtn', 'vodafone', 'airteltigo']
    CARD_SCHEMES = ['visa', 'mastercard']
    # Explicit manager declaration for static type checkers (e.g., Pylance)
    objects = models.Manager()
    
    phone_validator = RegexValidator(
        regex=r'^\d{12,13}$',
        message="Phone number must be 12-13 digits (e.g., 233244000000)"
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=WALLET_TYPE_CHOICES)
    account_number = models.CharField(max_length=20)
    account_scheme = models.CharField(max_length=20, choices=SCHEME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(
        max_length=13, 
        validators=[phone_validator],
        help_text="Phone number of wallet owner (e.g., 233244000000)"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['account_number', 'owner']),
        ]
        unique_together = ['account_number', 'owner']
    
    def clean(self):
        """Validate wallet type matches scheme"""
        super().clean()
        
        if self.type == 'momo' and self.account_scheme not in self.MOMO_SCHEMES:
            raise ValidationError({
                'account_scheme': f'For mobile money, scheme must be one of: {", ".join(self.MOMO_SCHEMES)}'
            })
        
        if self.type == 'card' and self.account_scheme not in self.CARD_SCHEMES:
            raise ValidationError({
                'account_scheme': f'For card, scheme must be one of: {", ".join(self.CARD_SCHEMES)}'
            })
    
    def save(self, *args, **kwargs):
        """Store only first 6 digits for card numbers"""
        self.full_clean()  # Run validation
        
        # Truncate card numbers to first 6 digits
        if self.type == 'card' and len(self.account_number) > 6:
            self.account_number = self.account_number[:6]
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.type}) - {self.owner}"

