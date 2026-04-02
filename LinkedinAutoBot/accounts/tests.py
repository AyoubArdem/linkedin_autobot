from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from .models import Membership, WorkSpace


User = get_user_model()


class AccountsModelTests(TestCase):
    def test_create_user_hashes_password(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="strongpass123",
            name="Test User",
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("strongpass123"))

    def test_membership_is_unique_per_user_and_workspace(self):
        user = User.objects.create_user(
            email="member@example.com",
            password="strongpass123",
            name="Member User",
        )
        workspace = WorkSpace.objects.create(name="Primary", owner=user)

        Membership.objects.create(user=user, workspace=workspace)

        with self.assertRaises(IntegrityError):
            Membership.objects.create(user=user, workspace=workspace)

    def test_backfill_api_keys_command_sets_missing_keys(self):
        user = User.objects.create_user(
            email="nokey@example.com",
            password="strongpass123",
            name="No Key User",
        )
        user.api_key = None
        user.save(update_fields=["api_key"])

        call_command("backfill_api_keys")

        user.refresh_from_db()
        self.assertTrue(user.api_key)
