# ===================== wallet/views/paystack.py =====================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import User
from .utils.paystack import initialize_transaction, charge_authorization

class InitializeMandateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.authorization_code:
            return Response({"message": "Mandate already initialized."})
        response_data = initialize_transaction(user.email, 10000)  # dummy amount
        if response_data.get("status"):
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class ChargeUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get("amount")
        if not user.authorization_code:
            return Response({"error": "User has not authorized direct debit."}, status=status.HTTP_403_FORBIDDEN)

        response_data = charge_authorization(user.email, amount, user.authorization_code)
        return Response(response_data, status=status.HTTP_200_OK)