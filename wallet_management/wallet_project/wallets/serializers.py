from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Standard serializer for listing and retrieving wallets
    
    Used for:
    - GET /api/wallets/ (list)
    - GET /api/wallets/{id}/ (retrieve)
    """
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    scheme_display = serializers.CharField(source='get_account_scheme_display', read_only=True)
    
    class Meta:
        model = Wallet
        fields = [
            'id',
            'name',
            'type',
            'account_number',
            'account_scheme',
            'created_at',
            'owner_phone'
        ]
        read_only_fields = ['id', 'created_at', 'owner_phone']


class WalletCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = ['name', 'type', 'account_number', 'account_scheme']
    
    def validate_account_number(self, value):
        """Validate account number format"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Account number cannot be empty")
        
        # Remove any spaces or dashes
        cleaned_value = value.replace(' ', '').replace('-', '')
        
        # Basic length validation
        if len(cleaned_value) < 6:
            raise serializers.ValidationError("Account number is too short")
        
        return cleaned_value
    
    def validate(self, data):
        """
        Comprehensive validation for wallet creation
        
        Validates:
        1. Type-scheme compatibility
        2. Duplicate prevention
        3. 5-wallet limit per user
        """
        request = self.context.get('request')
        
        if not request or not request.user:
            raise serializers.ValidationError("Authentication required")
        
        owner = request.user.username
       
        
        # RULE 1: Validate type and scheme match
        wallet_type = data.get('type')
        account_scheme = data.get('account_scheme')
        
        if wallet_type == 'momo' and account_scheme not in Wallet.MOMO_SCHEMES:
            raise serializers.ValidationError({
                'account_scheme': f"For mobile money wallets, scheme must be one of: {', '.join(Wallet.MOMO_SCHEMES)}"
            })
        
        if wallet_type == 'card' and account_scheme not in Wallet.CARD_SCHEMES:
            raise serializers.ValidationError({
                'account_scheme': f"For card wallets, scheme must be one of: {', '.join(Wallet.CARD_SCHEMES)}"
            })
        
       
        
        # RULE 2: Check for duplicate wallet (same account_number + owner)
        account_number = data.get('account_number')
        
        # For cards, check first 6 digits only (since that's what gets stored)
        if wallet_type == 'card' and len(account_number) > 6:
            check_account_number = account_number[:6]
        else:
            check_account_number = account_number
        
        if Wallet.objects.filter(account_number=check_account_number, owner=owner).exists():
            raise serializers.ValidationError({
                'account_number': 'You already have a wallet with this account number.'
            })
        
       
        
        # RULE 3: Check 5-wallet limit
        wallet_count = Wallet.objects.filter(owner=owner).count()
        if wallet_count >= 5:
            raise serializers.ValidationError(
                'You cannot have more than 5 wallets. Please delete an existing wallet before adding a new one.'
            )
          
        return data
    
    def create(self, validated_data):
        """
        Create wallet and automatically set owner from authenticated user
        """
        request = self.context.get('request')
        validated_data['owner'] = request.user.username
        return super().create(validated_data)
        
