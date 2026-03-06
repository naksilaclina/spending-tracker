from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

import jwt
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from apps.authn.services import VerifiedToken
from apps.users.models import UserProfile

User = get_user_model()


@pytest.mark.django_db
def test_auth_me_syncs_user_from_verified_supabase_claims():
    client = APIClient()
    claims = {
        "sub": "supabase-user-1",
        "email": "user@example.com",
        "exp": 9999999999,
        "user_metadata": {"display_name": "Casey"},
    }
    with patch("apps.authn.authentication.get_token_verifier") as mocked:
        mocked.return_value.verify.return_value = VerifiedToken(
            subject="supabase-user-1",
            email="user@example.com",
            claims=claims,
        )
        response = client.get("/api/v1/auth/me", HTTP_AUTHORIZATION="Bearer fake-token")

    assert response.status_code == 200
    profile = UserProfile.objects.get(supabase_user_id="supabase-user-1")
    assert profile.email == "user@example.com"
    assert response.json()["display_name"] == "Casey"


@pytest.mark.django_db
def test_missing_bearer_token_is_rejected():
    client = APIClient()
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403
