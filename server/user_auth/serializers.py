from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup
    Includes password confirmation
    """

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, data):
        """
        Check if passwords match and validate the password.
        """
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords do not match.")
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
