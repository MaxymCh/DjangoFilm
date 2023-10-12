from django import forms
from lesFilms.models import Film, Realisateur, Acteur
from django.forms import inlineformset_factory

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]

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
    
    def clean_titre(self):
        titre_original = self.cleaned_data['titre']
        titre = self.cleaned_data['titre'].lower()
        close_matches = []
        titres_similaires = Film.objects.exclude(pk=self.instance.pk if self.instance else None)
        max_length_difference = 2
        if titres_similaires.exists():
            self.titres_similaires = [film.titre.lower() for film in titres_similaires]
            for titre_proche in self.titres_similaires:
                length_difference = abs(len(titre) - len(titre_proche))
                if titre in titre_proche or titre_proche in titre:
                    if " " in titre:
                        max_length_difference = 3
                        if length_difference <= max_length_difference:
                            close_matches.append(titre_proche)
                    elif length_difference <= max_length_difference:
                        close_matches.append(titre_proche)
                elif levenshtein_distance(titre, titre_proche) <= 1:
                    close_matches.append(titre_proche)
        if close_matches != []:
            formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
            raise forms.ValidationError(f"Attention, d'autres films portent approximativement le même titre : {formatted_matches}")
        return titre_original


class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"


class ActeurForm(forms.ModelForm):
    class Meta:
        model = Acteur
        fields = "__all__"
    
    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        prenom = cleaned_data.get('prenom')
        nom_prenom = f"{nom.lower()} {prenom.lower()}"


        if not nom or not prenom:
            return cleaned_data
        
        close_matches = []
        max_length_difference = 2

        acteurs_similaires = Acteur.objects.exclude(pk=self.instance.pk if self.instance else None)
        if acteurs_similaires.exists():
            self.acteurs_similaires = [f"{acteur.nom.lower()} {acteur.prenom.lower()}" for acteur in acteurs_similaires]
            for acteur_proche in self.acteurs_similaires:
                length_difference = abs(len(nom_prenom) - len(acteur_proche))
                if nom_prenom in acteur_proche or acteur_proche in nom_prenom:
                    if length_difference <= max_length_difference:
                        close_matches.append(acteur_proche)
                    elif length_difference <= max_length_difference:
                        close_matches.append(acteur_proche)
                elif levenshtein_distance(nom_prenom, acteur_proche) <= 1:
                    close_matches.append(acteur_proche)
        if close_matches != []:
            formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
            raise forms.ValidationError(f"Attention, un acteur similaire est déjà enregistré : {formatted_matches}")
        return cleaned_data