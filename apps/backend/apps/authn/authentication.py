from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from apps.authn.services import get_token_verifier
from apps.users.services import UserSyncService


class SupabaseJWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode("utf-8")
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise AuthenticationFailed("Authorization header must use Bearer token.")

        verified = get_token_verifier().verify(parts[1])
        user = UserSyncService().sync_from_claims(verified)
        return user, verified.claims
