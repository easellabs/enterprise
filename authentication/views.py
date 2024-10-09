import logging
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from authentication.permissions import IsAdmin
from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer, RegisterSerializer, CustomUserSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django_otp.decorators import otp_required
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.password_validation import get_password_validators

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


User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    @otp_required
    def post(self, request):
        return Response({"message": "OTP verified successfully"})

@api_view(['POST'])
def enable_2fa(request):
    if request.method == 'POST':
        user = request.user
        if not hasattr(user, 'totp_device'):
            # Create TOTP Device
            totp_device = TOTPDevice.objects.create(user=user, confirmed=False)
            # Generate QR Code URL
            qr_code_url = totp_device.config_url
            return Response({'qr_code_url': qr_code_url})
        return Response({'message': '2FA already enabled'}, status=400)

@api_view(['POST'])
def verify_2fa(request):
    if request.method == 'POST':
        user = request.user
        otp = request.data.get('otp')
        totp_device = getattr(user, 'totp_device', None)
        if totp_device and totp_device.verify_token(otp):
            # Generate tokens after successful 2FA
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'message': 'Invalid OTP'}, status=400)












class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    throttle_classes = [AnonRateThrottle]  # Throttle to prevent anonymous abuse

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    self._send_welcome_email(user)
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    logger.info(f"User '{user.username}' registered successfully.")
                    return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                return Response({"error": "Internal server error. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _send_welcome_email(self, user):
        try:
            send_mail(
                'Welcome to CarbonR Platform',
                'You have successfully registered.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info(f"Welcome email sent to {user.email}.")
        except Exception as email_error:
            logger.error(f"Failed to send email to {user.email}: {email_error}")


class RegisterAdminUserView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['role'] = 'Admin'
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save(is_staff=True)
                    user.userprofile.role = 'Admin'
                    user.userprofile.save()
                    logger.info(f"Admin user '{user.username}' created successfully.")
                    return Response({"message": "Admin user created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating admin user: {e}")
                return Response({"error": "Internal server error. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.warning(f"Admin user registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user '{request.user.username}'")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User profile updated for user '{request.user.username}'.")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.warning(f"User profile update failed for user '{request.user.username}': {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user '{request.user.username}'")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)


class ListUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class ManageUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'


class UserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            data = {
                "message": "Welcome to the User Dashboard",
                "user": {
                    "username": request.user.username,
                    "email": request.user.email,
                    "role": request.user.userprofile.role,
                }
            }
            logger.info(f"User '{request.user.username}' accessed the dashboard.")
            return Response(data, status=status.HTTP_200_OK)
        except AttributeError:
            logger.error(f"UserProfile not found for user '{request.user.username}'")
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = {
            "admin_details": {
                "username": request.user.username,
                "role": "Admin",
                "total_users": User.objects.count()
            }
        }
        logger.info(f"Admin '{request.user.username}' accessed the admin dashboard.")
        return Response(data, status=status.HTTP_200_OK)


class AdminOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        logger.info(f"Admin-only access by user '{request.user.username}'")
        return Response({"message": "Hello, Admin!"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                logger.warning(f"Logout failed: No refresh token provided by user '{request.user.username}'")
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User '{request.user.username}' logged out successfully.")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Error during logout for user '{request.user.username}': {e}")
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """
    View to handle user login.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            logger.warning("Login failed: Missing username or password.")
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            logger.info(f"User '{username}' logged in successfully.")
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        logger.warning(f"Login failed for username '{username}': Invalid credentials.")
        raise AuthenticationFailed("Invalid credentials")
