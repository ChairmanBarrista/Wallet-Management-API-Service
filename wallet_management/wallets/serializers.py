from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'user')

    def validate(self, data):
        user = self.context['request'].user

        # 1. Max 5 wallets per user
        if Wallet.objects.filter(user=user).count() >= 5:
            raise serializers.ValidationError("A user cannot have more than 5 wallets.")

        # 2. Prevent duplicate wallets
        if Wallet.objects.filter(
            user=user,
            account_number=data['account_number'][:6],
            account_scheme=data['account_scheme']
        ).exists():
            raise serializers.ValidationError("Duplicate wallet detected.")

        return data

    def create(self, validated_data):
        # Store only first 6 digits
        validated_data['account_number'] = validated_data['account_number'][:6]
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
