from django import forms
from lesFilms.models import Film, Realisateur, Acteur

class FilmForm(forms.ModelForm):
    date_creation = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    realisateur_nom = forms.CharField(max_length=100, required=False, label="Nom du réalisateur")
    realisateur_prenom = forms.CharField(max_length=100, required=False, label="Prénom du réalisateur")
    acteurs = forms.ModelMultipleChoiceField(
            queryset=Acteur.objects.all(),
            required=False,  # Ici, on précise que le champ n'est pas requis
            widget=forms.SelectMultiple(attrs={'class': 'your-css-class', 'required': False})
    )
    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.initial["date_creation"] = self.instance.formatted_date()
            self.initial["realisateur_nom"] = self.instance.realisateur.nom
            self.initial["realisateur_prenom"] = self.instance.realisateur.prenom        
            self.fields['acteurs'].required = False  # Indiquer que le champ 'acteurs' n'est pas requis
    class Meta:
        model = Film
        fields = ['titre', 'description', 'date_creation', 'realisateur_nom', 'realisateur_prenom', 'acteurs']
    
class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"
    
class ActeurForm(forms.ModelForm):
    class Meta:
        model = Acteur
        fields = "__all__"
    
