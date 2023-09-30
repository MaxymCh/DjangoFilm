from django import forms
from lesFilms.models import Film


class FilmForm(forms.ModelForm):
    date_creation = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Film
        fields = "__all__"
