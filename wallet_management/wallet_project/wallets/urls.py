from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet

# Create router and register viewset
router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
