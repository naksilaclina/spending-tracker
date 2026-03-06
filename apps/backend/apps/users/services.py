from django.contrib.auth import get_user_model
from django.db import transaction

from apps.authn.services import VerifiedToken
from apps.users.models import UserProfile

User = get_user_model()


class UserSyncService:
    @transaction.atomic
    def sync_from_claims(self, verified: VerifiedToken):
        email = verified.email or f"{verified.subject}@users.local"
        user, _ = User.objects.get_or_create(
            username=verified.subject,
            defaults={"email": email},
        )
        if user.email != email:
            user.email = email
            user.save(update_fields=["email"])

        display_name = (
            verified.claims.get("user_metadata", {}).get("display_name")
            or verified.claims.get("app_metadata", {}).get("display_name")
            or ""
        )
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "supabase_user_id": verified.subject,
                "email": email,
                "display_name": display_name,
            },
        )
        dirty_fields = []
        if profile.supabase_user_id != verified.subject:
            profile.supabase_user_id = verified.subject
            dirty_fields.append("supabase_user_id")
        if profile.email != email:
            profile.email = email
            dirty_fields.append("email")
        if display_name and profile.display_name != display_name:
            profile.display_name = display_name
            dirty_fields.append("display_name")
        if dirty_fields:
            profile.save(update_fields=dirty_fields)
        return user
