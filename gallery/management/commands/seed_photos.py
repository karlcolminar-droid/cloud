from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gallery.models import RecipePhoto

User = get_user_model()

SAMPLE_PHOTOS = [
    {
        "title": "Shakshuka",
        "description": "Middle Eastern dish of eggs poached in spicy tomato sauce with fresh parsley.",
    },
    {
        "title": "Pansit Canton",
        "description": "Filipino stir-fried noodle dish with meat, vegetables, and savory sauce.",
    },
    {
        "title": "Bopis",
        "description": "Filipino chopped meat stew with liver, heart, and diced vegetables in gravy.",
    },
    {
        "title": "Bola Bola",
        "description": "Filipino meat balls in a savory tomato-based sauce, served with dipping sauce.",
    },
]


class Command(BaseCommand):
    help = "Seed database with sample RecipePhoto entries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default="admin",
            help="Username of the owner for sample photos (default: admin)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing sample photos before seeding",
        )

    def handle(self, *args, **options):
        username = options["username"]
        try:
            owner = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User '{username}' does not exist. Create it first.")
            )
            return

        if options["clear"]:
            RecipePhoto.objects.filter(owner=owner).delete()
            self.stdout.write(self.style.SUCCESS(f"Cleared photos owned by {username}"))

        created_count = 0
        for photo_data in SAMPLE_PHOTOS:
            # Only create if not already present
            if not RecipePhoto.objects.filter(
                title=photo_data["title"], owner=owner
            ).exists():
                RecipePhoto.objects.create(owner=owner, **photo_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {photo_data['title']}")
                )
            else:
                self.stdout.write(f"Skipped: {photo_data['title']} (already exists)")

        self.stdout.write(
            self.style.SUCCESS(f"\nTotal created: {created_count} photos")
        )
        self.stdout.write(
            self.style.WARNING(
                "\nNote: Images are empty. Upload photos via the web interface or add image URLs to RecipePhoto."
            )
        )
