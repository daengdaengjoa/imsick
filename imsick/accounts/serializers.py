from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "nickname", "age", "gender", "point"]

class UserCreateSerializer(UserUpdateSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username", "password", "confirm_password", "email", "name",
            "nickname", "age", "gender", "point"
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, data):
        password = data.get("password")
        username = data.get("username")
        confirm_password = data.pop("confirm_password", None)

        if username == password:
            raise serializers.ValidationError("아이디와 비밀번호를 다르게 입력해주세요.")
        if not password:
            raise serializers.ValidationError("비밀번호를 입력해주세요.")
        if password != confirm_password:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        validate_password(password)
        return data



class UserPasswordSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ["password", "confirm_password"]

    def validate(self, data):
        new_password = data.get("password")
        password = data.get("password")
        confirm_password = data.pop("confirm_password", None)
        validate_password(new_password)
        user = self.instance
        if user and check_password(new_password, user.password):
            raise ValidationError("비밀번호가 이전과 같습니다.")
        if not password:
            raise serializers.ValidationError("비밀번호를 입력해주세요.")
        if password != confirm_password:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        validate_password(password)
        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data["password"])
        instance.save()
        return instance
