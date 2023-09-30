import os
import django

django.setup()

from lesFilms.models import Film


def populate_database():
    # Liste de données de films à insérer
    films_data = [
        {
            "titre": "Inception",
            "description": "Un voleur professionnel entre dans les rêves des gens pour leur voler des idées.",
            "realisateur": "Christopher Nolan",
        },
        {
            "titre": "Pulp Fiction",
            "description": "Les vies de plusieurs criminels de Los Angeles s'entrecroisent de manière imprévisible.",
            "realisateur": "Quentin Tarantino",
        },
        {
            "titre": "La La Land",
            "description": "Un musicien et une actrice tombent amoureux tout en essayant de réaliser leurs rêves à Los Angeles.",
            "realisateur": "Damien Chazelle",
        },
        {
            "titre": "Parasite",
            "description": "Une famille pauvre infiltre la vie d'une famille riche, avec des conséquences imprévues.",
            "realisateur": "Bong Joon-ho",
        },
        {
            "titre": "Interstellar",
            "description": "Un groupe d'explorateurs voyage à travers un trou de ver près de Saturne pour trouver un nouvel habitat pour l'humanité.",
            "realisateur": "Christopher Nolan",
        },
    ]

    # Insertion des films dans la base de données
    for film_data in films_data:
        film = Film(**film_data)
        film.save()


if __name__ == "__main__":
    populate_database()
