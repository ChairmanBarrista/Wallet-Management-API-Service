from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wallet
from .serializers import WalletSerializer, WalletCreateSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user wallets
    
    Endpoints:
    - POST /api/wallets/ - Create a new wallet
    - GET /api/wallets/ - List all user's wallets
    - GET /api/wallets/{id}/ - Retrieve a specific wallet
    - DELETE /api/wallets/{id}/ - Delete a wallet
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return wallets for the authenticated user only"""
        return Wallet.objects.filter(owner=self.request.user.username)
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return WalletCreateSerializer
        return WalletSerializer
    
    def create(self, request, *args, **kwargs):
        """
        POST /api/wallets/
        Create a new wallet with business rule validations
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            wallet = serializer.save()
            response_serializer = WalletSerializer(wallet)
            return Response(
                {
                    'message': 'Wallet created successfully',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'message': 'Wallet creation failed',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        """
        GET /api/wallets/
        List all wallets for the authenticated user
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Wallets retrieved successfully',
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/wallets/{id}/
        Retrieve a specific wallet by ID
        """
        wallet = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        serializer = self.get_serializer(wallet)
        
        return Response({
            'message': 'Wallet retrieved successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/wallets/{id}/
        Delete a specific wallet
        """
        wallet = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        wallet_name = wallet.name
        wallet.delete()
        
        return Response({
            'message': f'Wallet "{wallet_name}" deleted successfully'
        }, status=status.HTTP_200_OK)