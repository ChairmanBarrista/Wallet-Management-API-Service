from django.urls import path
from .views import *

urlpatterns = [
    path('wallets/', WalletListView.as_view()),
    path('wallets/create/', WalletCreateView.as_view()),
    path('wallets/<int:pk>/', WalletDetailView.as_view()),
    path('wallets/<int:pk>/delete/', WalletDeleteView.as_view()),
]
