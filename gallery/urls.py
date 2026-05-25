from django.urls import path
from .views import PhotoListView, PhotoUpdateView, PhotoDeleteView

urlpatterns = [
    path('', PhotoListView.as_view(), name='gallery_home'),
    path('recipe/<int:pk>/edit/', PhotoUpdateView.as_view(), name='edit_recipe'),
    path('recipe/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete_recipe'),
]

