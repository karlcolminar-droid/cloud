from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Create or update the default superuser."

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        username = os.getenv('ADMIN_USER', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@gmail.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" {action}.'))
