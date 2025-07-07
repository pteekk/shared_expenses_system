# ===================== shared_expense/models.py =====================

from django.db import models
from group.models import Group
from users.models import User

EXPENSE_TYPE_CHOICES = (
    ("instant", "Instant"),
    ("planned", "Planned"),
)

class SharedExpense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES)
    amount = models.PositiveIntegerField()
    disbursement_date = models.DateTimeField()
    lock_time = models.DateTimeField()
    recipient_name = models.CharField(max_length=100)
    recipient_bank = models.CharField(max_length=100)
    recipient_account = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)

class ExpenseMember(models.Model):
    shared_expense = models.ForeignKey(SharedExpense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    declined = models.BooleanField(default=False)