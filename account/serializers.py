from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoCoreValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User as AccountUser


class PersonalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ["id", "username", "first_name", "last_name", "email", "last_login"]
        read_only_fields = fields


class AccountPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "last_login",
        ]
        read_only_fields = fields


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "last_login",
        ]
        read_only_fields = ["id", "last_login"]

    def create(self, validated_data):
        password = validated_data.get("password")
        try:
            validate_password(password)
        except DjangoCoreValidationError as err:
            err_msg = " ".join(err.messages)
            raise ValidationError(
                {"detail": err_msg}, code="invalid_password"
            ) from None
        validated_data["password"] = make_password(password)
        user = AccountUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        if validated_data.get("password"):
            password = make_password(validated_data.get("password"))
            instance.password = password
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_stuff = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance
