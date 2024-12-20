from django.urls import path
from .views import AuthView, LogoutAllView

urlpatterns = [
    path("signup", AuthView.as_view(), name="signup"),  # Sign up
    path("login", AuthView.as_view(), name="login"),  # Log in
    path("logout_all", LogoutAllView.as_view(), name="logout_all"),  # Logout all
]
