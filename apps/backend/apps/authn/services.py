from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import jwt
from django.conf import settings
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError, PyJWKClientError
from rest_framework.exceptions import AuthenticationFailed


@dataclass(frozen=True)
class VerifiedToken:
    subject: str
    email: str
    claims: dict[str, Any]


class SupabaseTokenVerifier:
    def __init__(self) -> None:
        self.jwks_client = PyJWKClient(settings.SUPABASE_JWKS_URL) if settings.SUPABASE_JWKS_URL else None

    def _decode_hs256(self, token: str) -> dict[str, Any]:
        if not settings.SUPABASE_JWT_SECRET:
            raise AuthenticationFailed("Supabase JWT secret is not configured for HS256 verification.")
        issuer = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1" if settings.SUPABASE_URL else None
        return jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            issuer=issuer,
            options={"require": ["exp", "sub"]},
        )

    def verify(self, token: str) -> VerifiedToken:
        issuer = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1" if settings.SUPABASE_URL else None
        try:
            header = jwt.get_unverified_header(token)
            algorithm = header.get("alg", "RS256")
            if algorithm == "HS256":
                claims = self._decode_hs256(token)
            else:
                if not self.jwks_client:
                    raise AuthenticationFailed("Supabase JWKS URL is not configured.")
                signing_key = self.jwks_client.get_signing_key_from_jwt(token)
                claims = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=[algorithm],
                    audience=settings.SUPABASE_JWT_AUDIENCE,
                    issuer=issuer,
                    options={"require": ["exp", "sub"]},
                )
        except (InvalidTokenError, PyJWKClientError) as exc:
            raise AuthenticationFailed("Invalid or expired Supabase token.") from exc

        email = claims.get("email") or ""
        if not claims.get("sub"):
            raise AuthenticationFailed("Supabase token subject is missing.")
        return VerifiedToken(subject=claims["sub"], email=email, claims=claims)


@lru_cache(maxsize=1)
def get_token_verifier() -> SupabaseTokenVerifier:
    return SupabaseTokenVerifier()
