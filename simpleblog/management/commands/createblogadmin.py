from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Init Bot User"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        username = "blogadmin"
        try:
            blogadmin = User.objects.get(username=username)
        except User.DoesNotExist:
            blogadmin = User.objects.create_user(
                username=username,
                password="blogadmin_password",
                email="admin@example.com",
                first_name="Admin",
                is_staff=True,
                is_superuser=True,
            )
        blogadmin.save()
