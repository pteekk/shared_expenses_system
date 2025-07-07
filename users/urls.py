# ===================== users/urls.py =====================
from django.urls import path
from .views import UserSignupView, UserLoginView, UserProfileView, UserLogoutView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
# Add these to project urls.py with include('users.urls')