from django.urls import path
from . import auth_views
from django.contrib.auth import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", auth_views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path(
        "check-email/",
        auth_views.CheckDuplicateUsernameView.as_view(),
        name="check-email",
    ),
    path("email-verification/", auth_views.EmailVerification.as_view(), name="verify-email"),
    path('email-confirmation/', auth_views.EmailConfirmation.as_view(), name="activate"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password-change",
    ),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]