from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """Serializers for listing and retrieving wallets"""
    
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'type', 'account_number', 'account_scheme', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


class WalletCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating wallets with validation"""
    
    class Meta:
        model = Wallet
        fields = ['name', 'type', 'account_number', 'account_scheme']
    
    def validate(self, data):
        """Custom validation for wallet creation"""
        request = self.context.get('request')
        owner = request.user.username  # Assuming username is phone number
        
        # Validate type and scheme match
        if data['type'] == 'momo' and data['account_scheme'] not in Wallet.MOMO_SCHEMES:
            raise serializers.ValidationError({
                'account_scheme': f"For mobile money, scheme must be one of: {', '.join(Wallet.MOMO_SCHEMES)}"
            })
        
        if data['type'] == 'card' and data['account_scheme'] not in Wallet.CARD_SCHEMES:
            raise serializers.ValidationError({
                'account_scheme': f"For card, scheme must be one of: {', '.join(Wallet.CARD_SCHEMES)}"
            })
        
        # Check for duplicate wallet (same account_number + owner)
        if Wallet.objects.filter(account_number=data['account_number'], owner=owner).exists():
            raise serializers.ValidationError({
                'account_number': 'You already have a wallet with this account number.'
            })
        
        # Check 5-wallet limit
        wallet_count = Wallet.objects.filter(owner=owner).count()
        if wallet_count >= 5:
            raise serializers.ValidationError(
                'You cannot have more than 5 wallets. Please delete an existing wallet first.'
            )
        
        return data
   
    def create(self, validated_data):
        """Create wallet with owner from authenticated user"""
        request = self.context.get('request')
        validated_data['owner'] = request.user.username  # Set owner from authenticated user
        return super().create(validated_data)