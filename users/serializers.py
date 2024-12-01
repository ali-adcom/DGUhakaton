from django.core.validators import validate_email
from rest_framework import serializers

from config import OTP_LENGTH
from users.models import User, Family


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'family', 'gender', 'age')


class UserSignUpSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=OTP_LENGTH)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'otp', 'role', 'family', 'gender', 'age')

    def validate_email(self, value):
        validate_email(value)
        return value


class FamilyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'title', 'avatar', 'admin')


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'title', 'avatar', 'admin')
        read_only_fields = ('admin',)


class FamilyMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'gender', 'age')
