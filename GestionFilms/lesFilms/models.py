from django.db import models

# Create your models here.


class Film(models.Model):
    titre = models.CharField(max_length=250)
    description = models.TextField()
    date_creation = models.DateField()
    realisateur = models.CharField(max_length=250)

    def __str__(self):
        return f"Film {self.titre} de {self.realisateur}"
