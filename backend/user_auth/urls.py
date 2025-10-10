from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, logout_view

urlpatterns = [
    # POST /auth/register/ -----> Naya User Banane ke liye
    path('register/', RegisterView.as_view(), name='auth_register'),
    # POST /auth/login/ ------> Token (pass) lene ke liye
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # POST /auth/token/refresh/ ------> Token ko refresh karne ke liye
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='auth_logout'),
]