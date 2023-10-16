# pylint: disable=no-member

from django.test import TestCase
from .models import Film
import datetime

from django.test import TestCase
from .models import Realisateur, Acteur, Film
import datetime

class ModelTestCase(TestCase):
    def setUp(self):
        # Créez des instances de vos modèles ici
        self.realisateur = Realisateur.objects.create(nom="NomRealisateur", prenom="PrenomRealisateur")
        self.acteur = Acteur.objects.create(nom="NomActeur", prenom="PrenomActeur")
        self.film = Film.objects.create(
            titre="Titre Film",
            description="Description Film",
            date_creation=datetime.date.today(),
            realisateur=self.realisateur,
        )
        self.film.acteurs.add(self.acteur)

    def test_models_can_create_instances(self):
        """Teste la capacité des modèles à créer des instances."""
        self.assertEqual(self.realisateur.__str__(), "PrenomRealisateur NomRealisateur")
        self.assertEqual(self.acteur.__str__(), "PrenomActeur NomActeur")
        self.assertEqual(self.film.__str__(), "Film Titre Film de PrenomRealisateur NomRealisateur")
        self.assertEqual(self.film.formatted_date(), datetime.date.today().strftime("%Y-%m-%d"))


from django.urls import reverse
from django.test import TestCase, Client
from .models import Realisateur, Film


class FilmViewTestCase(TestCase):
    def test_film_creation(self):
        """Teste la création réussie d'un film."""
        nombre_de_film_initial = Film.objects.count()
        url = reverse('film_add')  # Remplacez par le nom réel de votre URL
        response = self.client.post(url, {
            'titre': 'Nouveau Film',
            'description': 'Description pour nouveau film',
            'date_creation': '2023-10-01',
            'realisateur_nom': 'RealisateurNom',
            'realisateur_prenom': 'RealisateurPrenom',
        })
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la création réussie
        nouveau_nombre_de_film = Film.objects.count()
        self.assertEqual(nombre_de_film_initial + 1, nouveau_nombre_de_film)

    def test_duplicate_film_title(self):
        """Teste la tentative de création d'un film avec un titre qui existe déjà."""
        url = reverse('film_add')
        # Créez d'abord un film pour simuler un titre existant
        response = self.client.post(url, {
            'titre': 'Nouveau Film',
            'description': 'Description pour nouveau film',
            'date_creation': '2023-10-01',
            'realisateur_nom': 'Jacques',
            'realisateur_prenom': 'Paul',
        })

        # Essayez de créer un film avec le même titre
        response_with_duplicate_title = self.client.post(url, {
            'titre': 'Nouveau Film',  # titre dupliqué
            'description': 'Autre description',
            'date_creation': '2023-10-02',
            'realisateur_nom': 'AutreNom',
            'realisateur_prenom': 'AutrePrenom',
        })
        # Ici, vous pouvez vérifier le code de statut ou un message d'erreur spécifique retourné par votre vue
        self.assertEqual(response_with_duplicate_title.status_code, 200)  # Aucune redirection, la création a échoué

        # Vérifiez que le nombre de films n'a pas changé
        self.assertEqual(Film.objects.count(), 1)