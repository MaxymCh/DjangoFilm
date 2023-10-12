# pylint: disable=no-member

# Create your views here.

from lesFilms.forms import FilmForm, RealisateurForm, ActeurForm
from lesFilms.models import Film, Realisateur, Acteur

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


# Film


class FilmCreate(CreateView):
    model = Film
    form_class = FilmForm
    template_name = "lesFilms/film/generic_form.html"
    success_url = reverse_lazy("film_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["action_name"] = "Création"
        context["action_description"] = "Entrez les informations du"
        context["realisateur_form"] = RealisateurForm(self.request.POST or None)
        context["acteur_from"] = ActeurForm(self.request.POST or None)


        return context

    def form_valid(self, form):   
        realisateur_nom = self.request.POST.get('realisateur_nom')
        realisateur_prenom = self.request.POST.get('realisateur_prenom')
        film = form.save(commit=False)

        try:
            realisateur = Realisateur.objects.get(nom=realisateur_nom, prenom=realisateur_prenom)
        except Realisateur.DoesNotExist:
            # Créez un nouvel acteur s'il n'existe pas (ou gérez l'erreur comme vous le souhaitez)
            realisateur = Realisateur(nom=realisateur_nom, prenom=realisateur_prenom)
            realisateur.save()

        film.realisateur = realisateur
        film.save()

        acteurs_ids = self.request.POST.getlist('acteurs')
        for acteur_id in acteurs_ids:
            acteur = Acteur.objects.get(pk=acteur_id)
            film.acteurs.add(acteur)

        self.object = film  # Assurez-vous que self.object est défini
        return HttpResponseRedirect(self.get_success_url())

class FilmUpdate(UpdateView):
    model = Film
    form_class = FilmForm

    template_name = "lesFilms/film/generic_form.html"
    success_url = reverse_lazy("film_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["action_name"] = "Modifier le"
        context["realisateur_form"] = RealisateurForm(self.request.POST or None)


        return context

    def form_valid(self, form):
        film = form.save()
        self.object = film  # Assurez-vous que self.object est défini
        return HttpResponseRedirect(self.get_success_url())


class FilmDeleteView(DeleteView):
    model = Film
    success_url = reverse_lazy("film_list")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class FilmListView(ListView):
    model = Film
    template_name = "lesFilms/film/film_list.html"  # Nom du template à utiliser
    context_object_name = "films"  # Nom de la variable à utiliser dans le template


def create_acteur_in_film(request):
    if request.method == "POST":
        form = ActeurForm(request.POST)
        if form.is_valid():
            acteur = form.save()
            return JsonResponse({"id": acteur.id, "name": str(acteur)})
        else:
            return JsonResponse({"error": "Invalid form data"}, status=400)

# Réalisateur


class RealisateurCreate(CreateView):
    model = Realisateur
    fields = "__all__"
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
    fields = "__all__"
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


#Acteur 



class ActeurCreate(CreateView):
    model = Acteur
    fields = "__all__"
    template_name = "lesFilms/acteur/generic_form.html"
    success_url = reverse_lazy("acteur_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["action_name"] = "Création"
        context["action_description"] = "Entrez les informations du"
        return context


class ActeurUpdate(UpdateView):
    model = Acteur
    fields = "__all__"
    template_name = "lesFilms/acteur/generic_form.html"
    success_url = reverse_lazy("acteur_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["action_name"] = "Modifier le"
        return context


class ActeurDeleteView(DeleteView):
    model = Acteur
    success_url = reverse_lazy("acteur_list")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ActeurListView(ListView):
    model = Acteur
    template_name = (
        "lesFilms/acteur/acteur_list.html"  # Nom du template à utiliser
    )
    context_object_name = (
        "acteurs"  # Nom de la variable à utiliser dans le template
    )
