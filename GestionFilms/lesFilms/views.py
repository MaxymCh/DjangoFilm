# pylint: disable=no-member

# Create your views here.

from lesFilms.forms import FilmForm, RealisateurForm
from lesFilms.models import Film, Realisateur

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.http import JsonResponse, HttpResponse


# Film


def film_add(request):
    if request.method == "POST":
        form = FilmForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse("film_show"))

            except:
                pass
    else:
        form = FilmForm()
    return render(request, "lesFilms/Film/add.html", {"form": form})


def film_show(request):
    films = Film.objects.all()
    return render(request, "lesFilms/Film/show.html", {"films": films})


def film_edit(request, id):
    film = Film.objects.get(id=id)
    return render(request, "lesFilms/Film/edit.html", {"film": film})


def film_update(request, id):
    film = Film.objects.get(id=id)
    form = FilmForm(request.POST, instance=film)
    if form.is_valid():
        form.save()
        return redirect(reverse("film_show"))
    return render(request, "lesFilms/Film/edit.html", {"film": film})


def film_delete(request, id):
    film = Film.objects.get(id=id)
    film.delete()
    return redirect(reverse("film_show"))


# Réalisateur


class RealisateurCreate(CreateView):
    model = Realisateur
    fields = ["nom", "prenom"]
    template_name = "lesFilms/realisateur/generic_form.html"
    success_url = reverse_lazy("realisateur_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["action_name"] = "Création"
        context["action_description"] = "Entrez les informations du"
        return context


class RealisateurUpdate(UpdateView):
    model = Realisateur
    fields = ["nom", "prenom"]
    template_name = "lesFilms/realisateur/generic_form.html"
    success_url = reverse_lazy("realisateur_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["action_name"] = "Modifier le"
        return context


class RealisateurDeleteView(DeleteView):
    model = Realisateur
    success_url = reverse_lazy("realisateur_list")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class RealisateurListView(ListView):
    model = Realisateur
    template_name = (
        "lesFilms/realisateur/realisateur_list.html"  # Nom du template à utiliser
    )
    context_object_name = (
        "realisateurs"  # Nom de la variable à utiliser dans le template
    )
