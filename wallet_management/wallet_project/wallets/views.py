from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from .serializers import WalletSerializer

class WalletCreateView(generics.CreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]


class WalletListView(generics.ListAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)


class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)


class WalletDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
