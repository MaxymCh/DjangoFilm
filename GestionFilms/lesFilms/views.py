# pylint: disable=no-member

# Create your views here.
from django import forms

from lesFilms.forms import FilmForm, RealisateurForm, ActeurForm
from lesFilms.models import Film, Realisateur, Acteur

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages

from Levenshtein import ratio



# Film


class FilmCreate(CreateView):
    model = Film
    form_class = FilmForm
    template_name = "lesFilms/film/generic_form.html"
    success_url = reverse_lazy("film_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_name"] = self.model.__name__
        context["acteur_form"] = ActeurForm(self.request.POST or None)


        return context

    def form_valid(self, form):   
        realisateur_nom = self.request.POST.get('realisateur_nom').capitalize()
        realisateur_prenom = self.request.POST.get('realisateur_prenom').capitalize()
        force_insertion = self.request.POST.get('force-insertion-film-real') is not None
        if not force_insertion:
            form_is_invalid = False
            titre_film = self.request.POST.get('titre')
            close_matches = []
            # Vérification en BD si similaire titre film
            titres_similaires = Film.objects.exclude(pk=self.object.pk if self.object else None)
            if titres_similaires.exists():
                self.titres_similaires = [film.titre.lower() for film in titres_similaires]
                for film_titre in self.titres_similaires:
                    if ratio(titre_film, film_titre) > 0.7:
                        close_matches.append(film_titre)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("titre",f"Attention, d'autres films portent approximativement le même titre : {formatted_matches}")
                form_is_invalid = True
            
            realisateur = Realisateur.objects.filter(nom=realisateur_nom, prenom=realisateur_prenom).first()
            if realisateur is None:
                nom_prenom = f"{realisateur_nom.capitalize()} {realisateur_prenom.capitalize()}"
                close_matches = []
                # Vérification en BD si similaire realisateur
                realisateurs = Realisateur.objects.exclude(pk=self.object.pk if self.object else None)
                if realisateurs.exists():
                    self.realisateurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in realisateurs]
                    for real in self.realisateurs_similaires:
                        if ratio(nom_prenom, real) > 0.8:
                            close_matches.append(real)
                # Si c'est le cas --> erreur
                if close_matches != []:
                    formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                    form.add_error("realisateur_nom",f"Attention, un réalisateur similaire est déjà enregistré : {formatted_matches}")
                    form_is_invalid = True          

            if(form_is_invalid):
                return self.form_invalid(form)
        if realisateur is None:
            realisateur = Realisateur(nom=realisateur_nom, prenom=realisateur_prenom)
        realisateur.save()

        film = form.save(commit=False)
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
        context["acteur_form"] = ActeurForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        realisateur_nom = self.request.POST.get('realisateur_nom').capitalize()
        realisateur_prenom = self.request.POST.get('realisateur_prenom').capitalize()
        force_insertion = self.request.POST.get('force-insertion-film-real') is not None
        realisateur = None
        if not force_insertion:
            form_is_invalid = False
            titre_film = self.request.POST.get('titre')
            close_matches = []
            # Vérification en BD si similaire titre film
            titres_similaires = Film.objects.exclude(pk=self.object.pk if self.object else None)
            if titres_similaires.exists():
                self.titres_similaires = [film.titre.lower() for film in titres_similaires]
                for film_titre in self.titres_similaires:
                    if ratio(titre_film, film_titre) > 0.7:
                        close_matches.append(film_titre)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("titre",f"Attention, d'autres films portent approximativement le même titre : {formatted_matches}")
                form_is_invalid = True
            
            realisateur = Realisateur.objects.filter(nom=realisateur_nom, prenom=realisateur_prenom).first()
            if realisateur is None:
                nom_prenom = f"{realisateur_nom.capitalize()} {realisateur_prenom.capitalize()}"
                close_matches = []
                # Vérification en BD si similaire realisateur
                realisateurs = Realisateur.objects.exclude(pk=self.object.pk if self.object else None)
                if realisateurs.exists():
                    self.realisateurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in realisateurs]
                    for real in self.realisateurs_similaires:
                        if ratio(nom_prenom, real) > 0.8:
                            close_matches.append(real)
                # Si c'est le cas --> erreur
                if close_matches != []:
                    formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                    form.add_error("realisateur_nom",f"Attention, un réalisateur similaire est déjà enregistré : {formatted_matches}")
                    form_is_invalid = True          

            if(form_is_invalid):
                return self.form_invalid(form)
        if realisateur is None:
            realisateur = Realisateur(nom=realisateur_nom, prenom=realisateur_prenom)
        realisateur.save()

        film = form.save(commit=False)
        film.realisateur = realisateur
        film.save()

        acteurs_ids = self.request.POST.getlist('acteurs')
        for acteur_id in acteurs_ids:
            acteur = Acteur.objects.get(pk=acteur_id)
            film.acteurs.add(acteur)

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
    paginate_by = 5


def create_acteur_in_film(request):
    if request.method == "POST":
        form = ActeurForm(request.POST)
        if(request.POST["force"] == "true"):
            acteur = form.save()
            return JsonResponse({"id": acteur.id, "name": str(acteur), "cree": True})            
        else:
            nom = request.POST.get('nom').capitalize()
            prenom = request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = []
            # Vérification en BD si similaire acteur
            acteurs = Acteur.objects.all()
            if acteurs.exists():
                acteurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in acteurs]
                for real in acteurs_similaires:
                    if ratio(nom_prenom, real) > 0.8:
                        close_matches.append(real)
            if close_matches == []:
                acteur = form.save()
                return JsonResponse({"id": acteur.id, "name": str(acteur), "cree": True})
            else:
                return JsonResponse({"liste_acteurs": close_matches, "cree": False})



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
    
    def form_valid(self, form):
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = []
            # Vérification en BD si similaire realisateur
            realisateurs = Realisateur.objects.exclude(pk=self.object.pk if self.object else None)
            if realisateurs.exists():
                self.realisateurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in realisateurs]
                for real in self.realisateurs_similaires:
                    if ratio(nom_prenom, real) > 0.8:
                        close_matches.append(real)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("nom",f"Attention, un réalisateur similaire est déjà enregistré : {formatted_matches}")
                return self.form_invalid(form)


        return super().form_valid(form)

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
    
    def form_valid(self, form):
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = []
            # Vérification en BD si similaire realisateur
            realisateurs = Realisateur.objects.exclude(pk=self.object.pk if self.object else None)
            if realisateurs.exists():
                self.realisateurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in realisateurs]
                for real in self.realisateurs_similaires:
                    if ratio(nom_prenom, real) > 0.8:
                        close_matches.append(real)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("nom",f"Attention, un réalisateur similaire est déjà enregistré : {formatted_matches}")
                return self.form_invalid(form)


        return super().form_valid(form)

class RealisateurDeleteView(DeleteView):
    model = Realisateur
    success_url = reverse_lazy("realisateur_list")
    
    def form_valid(self, form):
        realisateur_id = self.request.POST.get('id')
        if realisateur_id is not None:
            return super().form_valid(form)

        object = self.get_object()
        realisateur_id = self.kwargs.get('pk')
        realisateur = get_object_or_404(Realisateur, id=realisateur_id)

        # Vérification avant la suppression
        if realisateur.films.exists():
            return render(self.request, 'lesFilms/realisateur/realisateur_confirm_delete.html', {'object': realisateur})

        return super().form_valid(form)
        








class RealisateurListView(ListView):
    model = Realisateur
    template_name = (
        "lesFilms/realisateur/realisateur_list.html"  # Nom du template à utiliser
    )
    context_object_name = (
        "realisateurs"  # Nom de la variable à utiliser dans le template
    )
    paginate_by = 5



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
    
    def form_valid(self, form):
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = []
            # Vérification en BD si similaire acteur
            acteurs = Acteur.objects.exclude(pk=self.object.pk if self.object else None)
            if acteurs.exists():
                self.acteurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in acteurs]
                for real in self.acteurs_similaires:
                    if ratio(nom_prenom, real) > 0.8:
                        close_matches.append(real)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("nom",f"Attention, un acteur similaire est déjà enregistré : {formatted_matches}")
                return self.form_invalid(form)


        return super().form_valid(form)


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

    def form_valid(self, form):
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = []
            # Vérification en BD si similaire acteur
            acteurs = Acteur.objects.exclude(pk=self.object.pk if self.object else None)
            if acteurs.exists():
                self.acteurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in acteurs]
                for real in self.acteurs_similaires:
                    if ratio(nom_prenom, real) > 0.8:
                        close_matches.append(real)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("nom",f"Attention, un acteur similaire est déjà enregistré : {formatted_matches}")
                return self.form_invalid(form)


        return super().form_valid(form)


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
    paginate_by = 5

