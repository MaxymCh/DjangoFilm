from django import forms
from lesFilms.models import Film, Realisateur, Acteur
from django.forms import inlineformset_factory


class FilmForm(forms.ModelForm):
    date_creation = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    """acteur_nom = forms.CharField(max_length=100, required=False, label="Nom de l'acteur")
    acteur_prenom = forms.CharField(max_length=100, required=False, label="Prénom de l'acteur")"""


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["date_creation"] = self.instance.formatted_date()
    
    class Meta:
        model = Film
        fields = ['titre', 'description', 'date_creation', 'realisateur']

class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"


class ActeurForm(forms.ModelForm):
    class Meta:
        model = Acteur
        fields = "__all__"
