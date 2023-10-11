from django import forms
from lesFilms.models import Film, Realisateur, Acteur
from django.forms import inlineformset_factory
import numpy as np

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = np.arange(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances.append(distances[i1])
            else:
                distances.append(1 + min((distances[i1], distances[i1 + 1], distances[-1])))
        distances = distances
    return distances[-1]


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
        close_matches = []
        titres_similaires = Film.objects.filter(titre__icontains=titre)
        if titres_similaires.exists():
            self.titres_similaires = [film.titre for film in titres_similaires]
            for titre_proche in self.titres_similaires:
                if levenshtein_distance(titre, titre_proche) <= 1:
                    close_matches.append(titre_proche)
        if close_matches != []:
            raise forms.ValidationError(f"Attention, d'autres films portent approximativement le même titre : {str(close_matches)}")
        return titre


def filter_close_matches(target_title, titles_list):
    close_matches = []

    for title in titles_list:
        # Si la distance d'édition est 1 ou 0, considérez-le comme un match proche
        if levenshtein_distance(target_title, title) <= 1:
            close_matches.append(title)

    return close_matches

class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"


class ActeurForm(forms.ModelForm):
    class Meta:
        model = Acteur
        fields = "__all__"
