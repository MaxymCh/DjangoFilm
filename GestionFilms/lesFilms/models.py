from django.db import models

# Create your models here.


class Realisateur(models.Model):
    nom = models.CharField(max_length=250)
    prenom = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Acteur(models.Model):
    nom = models.CharField(max_length=250)
    prenom = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Film(models.Model):
    titre = models.CharField(max_length=250)
    description = models.TextField()
    date_creation = models.DateField()
    realisateur = models.ForeignKey(
        Realisateur, on_delete=models.CASCADE, related_name="films"
    )
    acteurs = models.ManyToManyField(Acteur, related_name="films")


    def __str__(self):
        return f"Film {self.titre} de {self.realisateur.prenom} {self.realisateur.nom}"

    def formatted_date(self):
        return self.date_creation.strftime("%Y-%m-%d")


