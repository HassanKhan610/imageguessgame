#forms.py
from dal import autocomplete
from django import forms
from .models import ImageGame

class ImageGameForm(forms.ModelForm):
    class Meta:
        model = ImageGame
        fields = ['title']

class ImageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ImageGame.objects.none()

        qs = ImageGame.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs
