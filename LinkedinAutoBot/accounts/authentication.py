from rest_framework import authentication, exceptions

from .models import User


class ApiKeyAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode("utf-8")
        api_key = ""

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == self.keyword:
                api_key = parts[1]

        if not api_key:
            api_key = request.headers.get("X-API-Key", "")

        if not api_key:
            return None

        user = User.objects.filter(api_key=api_key, is_active=True).first()
        if not user:
            raise exceptions.AuthenticationFailed("Invalid API key.")

        return (user, api_key)
