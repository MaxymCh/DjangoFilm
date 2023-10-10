from django import forms
from lesFilms.models import Film, Realisateur, Acteur
from django.forms import inlineformset_factory


class FilmForm(forms.ModelForm):
    date_creation = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["date_creation"] = self.instance.formatted_date()

    class Meta:
        model = Film
        fields = "__all__"

    def clean_titre(self):
        titre = self.cleaned_data['titre']
        titres_similaires = Film.objects.filter(titre__icontains=titre)
        if titres_similaires.exists():
            self.titres_similaires = [film.titre for film in titres_similaires]
        return titre

class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"


class ActeurForm(forms.ModelForm):
    class Meta:
        model = Acteur
        fields = "__all__"
