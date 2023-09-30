from django.urls import path
from . import views

urlpatterns = [
    path("", views.show),
    path("add", views.add, name="film_add"),
    path("show", views.show, name="film_show"),
    path("edit/<int:id>", views.edit, name="film_edit"),
    path("update/<int:id>", views.update, name="film_update"),
    path("delete/<int:id>", views.delete, name="film_delete"),
]
