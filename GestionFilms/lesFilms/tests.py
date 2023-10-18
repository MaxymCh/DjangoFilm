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

class ActeurViewTestCase(TestCase):
    def setUp(self):
        # Créez un acteur qui peut être utilisé dans plusieurs tests
        self.acteur = Acteur.objects.create(nom='Depardieu', prenom='Gerard')

    def test_realisateur_creation(self):
        """Teste la création réussie d'un acteur."""
        nombre_de_acteur_initial = Acteur.objects.count()  # Assurez-vous que acteur est importé depuis vos models
        url = reverse('acteur_add')  # Remplacez par le nom réel de votre URL pour ajouter un acteur

        # Données pour un nouveau acteur
        acteur_data = {
            'nom': 'NomDuRealisateur',
            'prenom': 'PrenomDuRealisateur',
        }

        # Soumettre la requête POST pour créer un nouveau acteur
        response = self.client.post(url, acteur_data)

        # Vérifier si la requête a été traitée avec succès (par exemple, si elle est redirigée vers une autre page)
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la création réussie

        # Vérifier si le nombre de acteurs dans la base de données a augmenté de 1
        nouveau_nombre_de_acteur = Acteur.objects.count()
        self.assertEqual(nombre_de_acteur_initial + 1, nouveau_nombre_de_acteur)

    def test_duplicate_acteur_name(self):
        """Teste la tentative de création d'un acteur avec un nom et prénom qui existent déjà."""
        url = reverse('acteur_add')  # Utilisez le nom réel de votre URL

        # Créez d'abord un acteur pour simuler un nom existant
        response = self.client.post(url, {
            'nom': 'Dupont',
            'prenom': 'Jean',
        })

        # Essayez de créer un acteur avec le même nom et prénom
        response_with_duplicate_name = self.client.post(url, {
            'nom': 'Dupont',  # nom dupliqué
            'prenom': 'Jean',  # prénom dupliqué
        })

        # Ici, vous pouvez vérifier le code de statut ou un message d'erreur spécifique retourné par votre vue
        self.assertEqual(response_with_duplicate_name.status_code, 200)  # Aucune redirection, la création a échoué

        # Vérifiez que le nombre de acteurs n'a pas changé
        self.assertEqual(Acteur.objects.count(), 2)
    
    def test_acteur_update(self):
        """Teste la mise à jour réussie d'un acteur."""
        url = reverse('acteur_edit', kwargs={'pk': self.acteur.pk})
        response = self.client.post(url, {
            'nom': 'Depardieu',
            'prenom': 'Gérard',
        })
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la mise à jour réussie
        self.acteur.refresh_from_db()
        self.assertEqual(self.acteur.prenom, 'Gérard')  # Assurez-vous que le prénom a bien été mis à jour

    def test_acteur_delete(self):
        """Teste la suppression réussie d'un acteur."""
        nombre_d_acteurs_initial = Acteur.objects.count()
        url = reverse('acteur_delete', kwargs={'pk': self.acteur.pk})
        response = self.client.post(url)  # La méthode DeleteView attend une requête POST
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la suppression réussie
        self.assertEqual(Acteur.objects.count(), nombre_d_acteurs_initial - 1)




class RealisateurViewTestCase(TestCase):
    def setUp(self):
        # Créez un acteur qui peut être utilisé dans plusieurs tests
        self.realisateur = Realisateur.objects.create(nom='Nolan', prenom='Christopher ')

    def test_realisateur_creation(self):
        """Teste la création réussie d'un réalisateur."""
        nombre_de_realisateur_initial = Realisateur.objects.count()  # Assurez-vous que Realisateur est importé depuis vos models
        url = reverse('realisateur_add')  # Remplacez par le nom réel de votre URL pour ajouter un réalisateur

        # Données pour un nouveau réalisateur
        realisateur_data = {
            'nom': 'NomDuRealisateur',
            'prenom': 'PrenomDuRealisateur',
        }

        # Soumettre la requête POST pour créer un nouveau réalisateur
        response = self.client.post(url, realisateur_data)

        # Vérifier si la requête a été traitée avec succès (par exemple, si elle est redirigée vers une autre page)
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la création réussie

        # Vérifier si le nombre de réalisateurs dans la base de données a augmenté de 1
        nouveau_nombre_de_realisateur = Realisateur.objects.count()
        self.assertEqual(nombre_de_realisateur_initial + 1, nouveau_nombre_de_realisateur)

    def test_duplicate_realisateur_name(self):
        """Teste la tentative de création d'un réalisateur avec un nom et prénom qui existent déjà."""
        url = reverse('realisateur_add')  # Utilisez le nom réel de votre URL

        # Créez d'abord un réalisateur pour simuler un nom existant
        response = self.client.post(url, {
            'nom': 'Dupont',
            'prenom': 'Jean',
        })

        # Essayez de créer un réalisateur avec le même nom et prénom
        response_with_duplicate_name = self.client.post(url, {
            'nom': 'Dupont',  # nom dupliqué
            'prenom': 'Jean',  # prénom dupliqué
        })

        # Ici, vous pouvez vérifier le code de statut ou un message d'erreur spécifique retourné par votre vue
        self.assertEqual(response_with_duplicate_name.status_code, 200)  # Aucune redirection, la création a échoué

        # Vérifiez que le nombre de réalisateurs n'a pas changé
        self.assertEqual(Realisateur.objects.count(), 2)

    def test_realisateur_update(self):
        """Teste la mise à jour réussie d'un réalisateur."""
        url = reverse('realisateur_edit', kwargs={'pk': self.realisateur.pk})
        response = self.client.post(url, {
            'nom': 'Acteur',
            'prenom': 'Nouveau',
        })
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la mise à jour réussie
        self.realisateur.refresh_from_db()
        self.assertEqual(self.realisateur.prenom, 'Nouveau')  # Assurez-vous que le prénom a bien été mis à jour

    def test_realisateur_delete(self):
        """Teste la suppression réussie d'un realisateur."""
        nombre_de_realisateur_initial = Realisateur.objects.count()
        url = reverse('realisateur_delete', kwargs={'pk': self.realisateur.pk})
        response = self.client.post(url)  # La méthode DeleteView attend une requête POST
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la suppression réussie
        self.assertEqual(Realisateur.objects.count(), nombre_de_realisateur_initial - 1)


class FilmViewTestCase(TestCase):

    def setUp(self):
        # Créez des instances de Realisateur, Acteur et Film qui peuvent être utilisées dans plusieurs tests
        self.realisateur = Realisateur.objects.create(nom='Besson', prenom='Luc')
        self.acteur = Acteur.objects.create(nom='De Niro', prenom='Robert')
        self.film = Film.objects.create(titre='Le Grand Bleu', description ='Description pour nouveau film', date_creation='2023-10-01', realisateur=self.realisateur)
        self.film.acteurs.add(self.acteur)

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
        self.assertEqual(Film.objects.count(), 2)
        
    def test_film_update(self):
        """Teste la mise à jour réussie d'un film."""
        url = reverse('film_edit', kwargs={'pk': self.film.pk})
        response = self.client.post(url, {
            'titre': 'Le Grand Bleu 2',
            'description': 'Autre description',
            'date_creation': '2023-11-02',
            'realisateur_nom': 'Besson',
            'realisateur_prenom': 'Luc',
            'acteurs': [self.acteur.pk],
            # Ajoutez tous les autres champs requis par votre formulaire de film
        })
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la mise à jour réussie
        self.film.refresh_from_db()
        self.assertEqual(self.film.titre, 'Le Grand Bleu 2')  # Assurez-vous que le titre a bien été mis à jour

    def test_film_delete(self):
        """Teste la suppression réussie d'un film."""
        initial_film_count = Film.objects.count()
        url = reverse('film_delete', kwargs={'pk': self.film.pk})
        response = self.client.post(url)  # La méthode DeleteView attend une requête POST
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la suppression réussie
        new_film_count = Film.objects.count()
        self.assertEqual(initial_film_count - 1, new_film_count)




