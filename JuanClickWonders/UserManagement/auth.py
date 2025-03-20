from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if not access_token:
            return None

        validated_token = self.get_validated_token(access_token)
        try:
            user = self.get_user(validated_token)
        except:
            return None

        return (user, validated_token)

