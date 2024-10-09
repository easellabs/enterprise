from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, password_validation


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include both username and password.")

        data['user'] = user
        return data


class Enable2FASerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class Verify2FASerializer(serializers.Serializer):
    code = serializers.CharField()
