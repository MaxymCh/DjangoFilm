from django import forms
from lesFilms.models import Film, Realisateur


class FilmForm(forms.ModelForm):
    date_creation = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Film
        fields = "__all__"


class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"
