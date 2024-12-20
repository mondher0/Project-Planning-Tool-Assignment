from django.urls import path
from .views import AuthView

urlpatterns = [
    path(
        "<str:action>", AuthView.as_view(), name="auth"
    ),  # Handles both signup and login
]
