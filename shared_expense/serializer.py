# ===================== shared_expense/serializers.py =====================
from rest_framework import serializers
from .models import SharedExpense, ExpenseMember

class SharedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedExpense
        fields = '__all__'

class ExpenseMemberApprovalSerializer(serializers.Serializer):
    expense_id = serializers.IntegerField()