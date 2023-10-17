# Projet Django: Gestionnaire de Collection Média - BUT 3 IUT Informatique d'Orléans 2023-2024

## Description du Projet
Ce projet Django consiste à gérer une collection de films, en incluant des informations telles que l'année de sortie, le titre, le réalisateur, et autres informations pertinentes. Il est divisé en trois étapes majeures, chacune ajoutant de nouvelles fonctionnalités et complexités au projet.

### Fonctionnalités :
- **CRUD (Création, Lecture, Mise à jour, Suppression) pour chaque modèle (Film, Réalisateur, Acteur).**
- Versionnage correct du projet avec des tags indiquant les différentes étapes.
- Tests unitaires pour chaque étape.
- Mise en oeuvre de Bootstrap 5 pour le styling.

## Configuration Initiale

1. Assurez-vous d'avoir Python (3.8 ou plus récent) installé sur votre machine. 
2. Clonez ce dépôt GitHub sur votre machine locale.`https://github.com/MaxymCh/DjangoFilm.git`
3. Naviguez vers le dossier du projet via la ligne de commande.
4. Créez un environnement virtuel Python en exécutant : `python -m venv env`
5. Activez l'environnement virtuel :
    - Windows: `.\env\Scripts\activate`
    - macOS/Linux: `source env/bin/activate`
6. Installez les dépendances nécessaires avec : `pip install -r requirements.txt`

## Lancer le Projet

1. Appliquez les migrations pour configurer la base de données avec : `python manage.py migrate`
2. Démarrez le serveur de développement avec : `python manage.py runserver`
3. Ouvrez votre navigateur web et accédez à : `http://127.0.0.1:8000/` pour voir l'application en action.

## Développement

- **Étape 0** :
    - Création du projet (configuration des urls, settings, etc.)
    - Création de l'application.
    - Création du modèle avec une unique table `Film` contenant le réalisateur + migration 0001.
    - Création des vues et des templates associés pour le CRUD des films (héritage de templates).

- **Étape 1** :
    - Modification du modèle avec une nouvelle table `Réalisateur` associée à `Film` + migration 0002.
    - Création des vues associées pour le CRUD sur cette table.
    - Création des templates associés.

- **Étape 2** :
    - Modification du modèle avec une nouvelle table `Acteur` associée à `Film` + migration.
    - L'ajout des acteurs (et éventuellement du réalisateur) en BD devra se faire uniquement via le formulaire de création d'un film.

## Tests

Pour chaque étape, des tests sont proposés pour assurer le bon fonctionnement des fonctionnalités implémentées. Vous pouvez exécuter ces tests en utilisant la commande suivante : `python manage.py test`.

## Contribuer

Ce projet suit les conventions de Git et utilise un système de versionnage basé sur les tags pour indiquer les différentes étapes du projet.



---

