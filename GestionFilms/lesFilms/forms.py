from django import forms
from lesFilms.models import Film, Realisateur, User
from django.forms import inlineformset_factory


class FilmForm(forms.ModelForm):
    date_creation = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["date_creation"] = self.instance.formatted_date()
        self.fields["realisateur"].queryset = (
            Realisateur.objects.all() | Realisateur.objects.none()
        )
        self.fields["realisateur"].choices = list(
            self.fields["realisateur"].choices
        ) + [("create", "Créer un réalisateur")]

    class Meta:
        model = Film
        fields = "__all__"

    def clean_realisateur(self):
        realisateur = self.cleaned_data.get("realisateur")
        if realisateur and str(realisateur.id) == "0":
            return None  # Acceptez la valeur "0" comme valide
        return realisateur


class RealisateurForm(forms.ModelForm):
    class Meta:
        model = Realisateur
        fields = "__all__"

class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
