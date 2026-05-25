from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'

    def ready(self):
        # Create Album Admin group after migrations complete to avoid DB access at import time
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from django.db.models.signals import post_migrate
        from .models import RecipePhoto

        def create_album_admin_group(sender, **kwargs):
            try:
                content_type = ContentType.objects.get_for_model(RecipePhoto)
                perms = Permission.objects.filter(content_type=content_type)
                group, created = Group.objects.get_or_create(name='Album Admin')
                group.permissions.set(perms)
            except Exception:
                pass

        post_migrate.connect(create_album_admin_group, sender=self)
