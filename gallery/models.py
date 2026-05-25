from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class RecipePhoto(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Use Cloudinary in production, fall back to local ImageField in development
    try:
        from django.conf import settings
        if getattr(settings, 'USE_CLOUDINARY', False):
            image = CloudinaryField()
        else:
            image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    except Exception:
        # If settings can't be imported for some reason, default to a plain ImageField
        image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
        blank=True,
    )

    def __str__(self):
        owner = self.owner.username if self.owner else 'unknown'
        return f"{self.title} ({owner})"