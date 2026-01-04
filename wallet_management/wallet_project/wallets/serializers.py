from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            'id',
            'name',
            'type',
            'account_number',
            'account_scheme',
            'owner',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user

        # Max 5 wallets rule
        if Wallet.objects.filter(user=user).count() >= 5:
            raise serializers.ValidationError(
                "You cannot have more than 5 wallets."
            )

        # Duplicate wallet check
        account_number = attrs['account_number'][:6]

        if Wallet.objects.filter(
            user=user,
            account_number=account_number,
            account_scheme=attrs['account_scheme']
        ).exists():
            raise serializers.ValidationError(
                "This wallet already exists."
            )

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['account_number'] = validated_data['account_number'][:6]
        return Wallet.objects.create(**validated_data)
