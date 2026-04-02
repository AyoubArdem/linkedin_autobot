from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate API keys for existing users that do not have one."

    def handle(self, *args, **options):
        user_model = get_user_model()
        manager = user_model.objects
        updated = 0

        for user in user_model.objects.filter(api_key__isnull=True):
            user.api_key = manager._generate_api_key()
            user.save(update_fields=["api_key"])
            updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Backfilled API keys for {updated} user(s).")
        )
