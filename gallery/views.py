from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
import cloudinary.uploader

from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import RecipePhoto
from .forms import RecipePhotoForm


class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        obj = None
        try:
            obj = self.get_object()
        except Exception:
            return False
        return getattr(obj, 'owner', None) == user


class PhotoListView(ListView):
    model = RecipePhoto
    template_name = 'gallery/home.html'
    context_object_name = 'photos'
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        qs = RecipePhoto.objects.all().order_by('-uploaded_at')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = kwargs.get('form', RecipePhotoForm())
        ctx['query'] = self.request.GET.get('q', '')
        return ctx

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to upload photos.')
            return redirect('login')

        form = RecipePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                photo = form.save(commit=False)
                photo.owner = request.user
                photo.save()
                messages.success(request, f"'{photo.title}' uploaded successfully.")
                return redirect('gallery_home')
            except Exception as exc:
                messages.error(request, f"Upload failed: {exc}")
                # fall through to re-render form with errors

        # If invalid, render list with the bound form (shows validation errors)
        self.object_list = self.get_queryset()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class PhotoUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = RecipePhoto
    form_class = RecipePhotoForm
    template_name = 'gallery/edit.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('gallery_home')

    def form_valid(self, form):
        # If a new image file was uploaded, try to remove the old image
        old = self.get_object()
        new_file = self.request.FILES.get('image')
        if new_file and old and getattr(old, 'image', None):
            try:
                public_id = getattr(old.image, 'public_id', None)
            except Exception:
                public_id = None
            if public_id:
                try:
                    cloudinary.uploader.destroy(public_id)
                except Exception:
                    pass
            else:
                try:
                    old.image.delete(save=False)
                except Exception:
                    pass
        response = super().form_valid(form)
        try:
            messages.success(self.request, f"'{self.get_object().title}' updated successfully.")
        except Exception:
            pass
        return response


class PhotoDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = RecipePhoto
    template_name = 'gallery/delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('gallery_home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title
        if getattr(self.object, 'image', None):
            try:
                public_id = getattr(self.object.image, 'public_id', None)
            except Exception:
                public_id = None
            if public_id:
                try:
                    cloudinary.uploader.destroy(public_id)
                except Exception:
                    pass
            else:
                try:
                    self.object.image.delete(save=False)
                except Exception:
                    pass
        self.object.delete()
        messages.success(request, f"'{title}' was completely deleted.")
        return redirect(self.success_url)