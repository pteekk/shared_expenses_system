# ===================== wallet/urls/paystack.py =====================
from django.urls import path
from .views.paystack import InitializeMandateView, ChargeUserView

urlpatterns = [
    path('init-mandate/', InitializeMandateView.as_view(), name='initiate_direct_debit'),
    path('charge/', ChargeUserView.as_view(), name='charge_user'),
]

# Include these in your main project or wallet urls