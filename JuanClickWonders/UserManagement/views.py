from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, UserProfileSerializer,
    UpdateProfileSerializer, UpdatePasswordSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        response = Response(
            {"message": "Login successful."}, status=status.HTTP_200_OK
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=str(refresh.access_token),
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(
            ),
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=str(refresh),
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(
            ),
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response.data['set_cookies'] = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(
                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response(
                {"message": "Logout successful."},
                status=status.HTTP_200_OK
            )

            response.delete_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
            )
            response.delete_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
            )

            return response

        except Exception:
            return Response(
                {"error": "Logout failed."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Password updated successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

        response.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
        )
        response.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
        )

        user.delete()
        return response


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"http://localhost:5173/reset-password/{uidb64}/{token}/"

        subject = "Password Reset Request"
        message = f"""
        Good day!

        You recently requested to reset your password.
        Please click the link below to reset your password:

        {reset_url}

        If you did not request a password reset, please ignore this email.

        Thank you!

        Best regards,
        Juan-Click Wonders Team
        """

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response(
            {"message": "Password reset email sent. Please check your inbox."},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK
        )


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if not refresh_token:
            return Response(
                {"error": "No refresh token found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)

            response = Response(
                {"message": "Token refreshed successfully."}, status=status.HTTP_200_OK
            )

            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=str(refresh.access_token),
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(
                ),
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                    refresh.blacklist()

                new_refresh = RefreshToken.for_user(
                    User.objects.get(id=refresh['user_id'])
                )

                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=str(new_refresh),
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(
                    ),
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                    domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )

            return response

        except TokenError:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_401_UNAUTHORIZED
            )
