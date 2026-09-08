import os
from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Creates a superuser from environment variables if one doesn't already exist"

    def handle(self, *args, **options):
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([email, username, password]):
            self.stdout.write("Superuser env vars not set, skipping.")
            return

        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(f"Superuser {email} already exists, skipping.")
            return

        CustomUser.objects.create_superuser(
            email=email,
            username=username,
            password=password
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} created."))