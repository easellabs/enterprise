from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

# Serializer for User Registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        otp = data.get('otp')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate the user
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        # Check if 2FA is enabled for the user
        if hasattr(user, 'totp_device'):
            totp_device = user.totp_device
            if not otp:
                raise serializers.ValidationError("OTP is required for users with 2FA enabled.")
            if not totp_device.verify_token(otp):
                raise serializers.ValidationError("Invalid OTP.")

        # If the authentication and OTP (if applicable) are successful, return user data
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', None)
        )
        return user

# Base UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'role', 'date_of_birth']


# Serializer for User with Profile (Nested)
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=_("This email is already taken."))]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=_("This username is already taken."))]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'profile']

    def update(self, instance, validated_data):
        # Update nested UserProfile
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        if profile_data:
            profile_serializer = UserProfileUpdateSerializer(instance.profile, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        instance.save()
        return instance


# Serializer for User Registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        # Use the create_user method from the CustomUser model manager to create a new user
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid email or password.")


# Serializer for Password Reset
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email',)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("There is no user registered with this email address."))
        return value


# Serializer for Changing Passwords
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        fields = ('old_password', 'new_password', 'new_password2')

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": _("Passwords do not match.")})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is incorrect."))
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


# Serializer for User Profile Update
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'role', 'date_of_birth']

    def update(self, instance, validated_data):
        # Update instance fields and save
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

# Serializer for Updating User Details with Nested Profile
class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileUpdateSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        # Update UserProfile fields if provided
        if profile_data:
            try:
                UserProfileUpdateSerializer().update(instance.profile, profile_data)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(_("User profile does not exist."))

        instance.save()
        return instance
