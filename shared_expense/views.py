# ===================== shared_expense/views.py =====================

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from .models import SharedExpense, ExpenseMember
from .serializers import SharedExpenseSerializer, ExpenseMemberApprovalSerializer
from users.models import User
from wallet.utils.paystack import initialize_transaction, charge_authorization

class CreateSharedExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SharedExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpenseMemberApprovalSerializer(data=request.data)
        if serializer.is_valid():
            expense_id = serializer.validated_data['expense_id']
            user = request.user

            try:
                expense = SharedExpense.objects.get(id=expense_id)
                member = ExpenseMember.objects.get(shared_expense=expense, user=user)

                if member.approved:
                    return Response({"message": "Already approved."}, status=status.HTTP_400_BAD_REQUEST)

                # FIRST TIME: Trigger mandate setup
                if not user.authorization_code:
                    mandate = initialize_transaction(user.email, 10000)  # dummy N100
                    return Response({"initiate_mandate": True, "paystack": mandate}, status=200)

                # CALCULATE CHARGES
                raw_amount = expense.amount
                paystack_fee = int(min((raw_amount * 1.5 / 100) + 100, 2500))
                service_fee = 100 if raw_amount <= 188000 else 300
                total = raw_amount + paystack_fee + service_fee

                # CHARGE NOW
                charge_response = charge_authorization(user.email, total, user.authorization_code)
                if charge_response.get("status"):
                    member.approved = True
                    member.approved_at = timezone.now()
                    member.save()
                    return Response({"message": "Approved and debited", "paystack": charge_response})
                else:
                    return Response(charge_response, status=400)

            except SharedExpense.DoesNotExist:
                return Response({"error": "Shared expense not found."}, status=404)
            except ExpenseMember.DoesNotExist:
                return Response({"error": "You are not a member of this expense."}, status=403)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)