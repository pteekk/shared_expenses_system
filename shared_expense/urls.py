# ===================== shared_expense/urls.py =====================
from django.urls import path
from .views import CreateSharedExpenseView, ApproveExpenseView

urlpatterns = [
    path('create/', CreateSharedExpenseView.as_view(), name='create_shared_expense'),
    path('approve/', ApproveExpenseView.as_view(), name='approve_shared_expense'),
]

# Add shared_expense.urls to project-level urls.py