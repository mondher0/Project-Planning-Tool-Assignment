from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from .serializers import SignupSerializer, LoginSerializer


class AuthView(APIView):
    """
    Authentication View to handle Signup and Login
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle either signup or login based on the endpoint.
        """
        if self.request.path.endswith("signup"):
            return self.signup(request)
        elif self.request.path.endswith("login"):
            return self.login(request)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    def signup(self, request):
        """
        User Signup
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        """
        User Login
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Authenticate user
            user = authenticate(username=user.username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login successful!",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """Logout All View"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout All - Blacklists all tokens for the authenticated user
        """
        user = request.user
        try:
            tokens = OutstandingToken.objects.filter(user=user)
            for token in tokens:
                # Blacklist each outstanding token
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(
                {"message": "Successfully logged out from all devices."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while logging out from all devices."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
