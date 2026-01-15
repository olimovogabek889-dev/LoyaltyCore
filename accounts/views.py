from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer


# =========================
# REGISTER
# =========================

class RegisterView(APIView):
    """
    POST:
    - Foydalanuvchini ro‘yxatdan o‘tkazadi
    - JWT access va refresh token qaytaradi
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                }
            }
        },
        tags=["Auth"],
        summary="Register new user"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED
        )


# =========================
# LOGIN
# =========================

class LoginView(TokenObtainPairView):
    """
    POST:
    - Login (username + password)
    - JWT access va refresh token qaytaradi
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Login user"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# =========================
# TOKEN REFRESH
# =========================

class RefreshTokenView(TokenRefreshView):
    """
    POST:
    - Refresh token orqali yangi access token oladi
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Refresh access token"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
