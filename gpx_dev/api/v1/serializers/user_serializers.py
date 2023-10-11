from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Общий сериализатор"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
            "birthday",
            "weight",
            "height",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор на создание пользователя"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "nickname",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "birthday",
            "weight",
            "height",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"], nickname=validated_data["nickname"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор на обновление пользователя"""

    class Meta:
        model = User
        fields = (
            "nickname",
            "first_name",
            "last_name",
            "birthday",
            "weight",
            "height",
        )
