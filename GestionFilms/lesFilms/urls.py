from django.urls import path
from . import views

urlpatterns = [
    path("", views.film_show),
    path("film/add", views.film_add, name="film_add"),
    path("film/show", views.film_show, name="film_show"),
    path("film/edit/<int:id>", views.film_edit, name="film_edit"),
    path("film/update/<int:id>", views.film_update, name="film_update"),
    path("film/delete/<int:id>", views.film_delete, name="film_delete"),
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
]
