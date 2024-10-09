# Updated views.py for core functionalities

import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from .serializers import RegisterSerializer, LoginSerializer, Enable2FASerializer, Verify2FASerializer

# Initialize logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registers a new user.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Logs in the user by validating the credentials.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enable_2fa(request):
    """
    Enables 2FA for the user.
    """
    user = request.user
    if not hasattr(user, 'totp_device'):
        totp_device = TOTPDevice.objects.create(user=user, confirmed=False)
        qr_code_url = totp_device.config_url
        return Response({'qr_code_url': qr_code_url}, status=status.HTTP_200_OK)
    return Response({'message': '2FA is already enabled'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa(request):
    """
    Verifies the OTP provided by the user.
    """
    user = request.user
    otp = request.data.get('otp')
    totp_device = getattr(user, 'totp_device', None)
    if totp_device and totp_device.verify_token(otp):
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
