from django.contrib import admin
from .models import RecipePhoto


@admin.register(RecipePhoto)
class RecipePhotoAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'uploaded_at')
	list_filter = ('uploaded_at',)
	search_fields = ('title', 'description', 'owner__username')
	readonly_fields = ('uploaded_at',)