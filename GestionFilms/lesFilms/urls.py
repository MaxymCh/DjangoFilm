from django.urls import path
from . import views

urlpatterns = [
    # Film
    path("", views.FilmListView.as_view(), name="film_list"),
    path("film/add", views.FilmCreate.as_view(), name="film_add"),
    path(
        "film/edit/<int:pk>",
        views.FilmUpdate.as_view(),
        name="film_edit",
    ),
    path(
        "film/delete/<int:pk>/",
        views.FilmDeleteView.as_view(),
        name="film_delete",
    ),
    path(
        "create_realisateur_in_film/",
        views.create_realisateur_in_film,
        name="create_realisateur_in_film",
    ),
    # Réalisateur
    path("realisateur/", views.RealisateurListView.as_view(), name="realisateur_list"),
    path("realisateur/add", views.RealisateurCreate.as_view(), name="realisateur_add"),
    path(
        "realisateur/edit/<int:pk>",
        views.RealisateurUpdate.as_view(),
        name="realisateur_edit",
    ),
    path(
        "realisateur/delete/<int:pk>/",
        views.RealisateurDeleteView.as_view(),
        name="realisateur_delete",
    ),
    # Acteur
    path("acteur/", views.ActeurListView.as_view(), name="acteur_list"),
    path("acteur/add", views.ActeurCreate.as_view(), name="acteur_add"),
    path(
        "acteur/edit/<int:pk>",
        views.ActeurUpdate.as_view(),
        name="acteur_edit",
    ),
    path(
        "acteur/delete/<int:pk>/",
        views.ActeurDeleteView.as_view(),
        name="acteur_delete",
    ),
]
