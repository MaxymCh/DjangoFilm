# pylint: disable=no-member

# Create your views here.
from django import forms

from lesFilms.forms import FilmForm, RealisateurForm, ActeurForm
from lesFilms.models import Film, Realisateur, Acteur

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from Levenshtein import ratio

def titre_similaire(self, titre):
    """
    La fonction `titre_similaire` vérifie si un titre de film donné est similaire à des titres de films
    existants dans la base de données et renvoie une liste de correspondances proches.
    
    :param titre: Le paramètre "titre" est le titre d'un film pour lequel on souhaite trouver des titres
    similaires
    :return: une liste de correspondances proches du titre donné.
    """
    close_matches = []

    # Vérification en BD si similaire titre film
    titres_similaires = Film.objects.exclude(pk=self.object.pk if self.object else None)
    titre = titre.lower()
    # Si il existe un film dans la base de données
    if titres_similaires.exists():
        self.titres_similaires = [film.titre.lower() for film in titres_similaires]
        for film_titre in self.titres_similaires:
            # Si un film similaire à 70% existe dans la base de données
            if ratio(titre, film_titre) > 0.7:

                # On ajoute dans les films similaires proches
                close_matches.append(film_titre)
    return close_matches

def realisateur_similaire(self, real_realisateur):
    """
    La fonction "réalisateur_similaire" vérifie si un réalisateur similaire existe dans la base de
    données et renvoie une liste de correspondances proches.
    
    :param real_realisateur: Le paramètre "real_realisateur" est le nom d'un réalisateur pour lequel
    vous souhaitez rechercher des réalisateurs similaires
    :return: une liste de correspondances proches du paramètre "real_realisateur" donné.
    """
    close_matches = []
    # Vérification en BD si similaire realisateur
    realisateurs = Realisateur.objects.exclude(pk=self.object.pk if self.object else None)

    # Si un réalisateur existe dans la base de données
    if realisateurs.exists():
        self.realisateurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in realisateurs]
        for real in self.realisateurs_similaires:

            # Si un réalisateur similaire à 80% existe dans la base de données
            if ratio(real_realisateur, real) > 0.8:

                # On ajoute dans les réalisateurs similaires proches
                close_matches.append(real)
    return close_matches

def acteur_similaire(self, acteur):
    """
    La fonction "acteur_similaire" vérifie s'il existe des acteurs similaires dans la base de données et
    renvoie une liste de correspondances proches.
    
    :param acteur: Le paramètre "acteur" représente le nom d'un acteur
    :return: une liste de correspondances proches de l'acteur donné.
    """
    close_matches = []
    # Vérification en BD si similaire acteur
    acteurs = Acteur.objects.exclude(pk=self.object.pk if self.object else None)
    if acteurs.exists():
        self.acteurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in acteurs]
        for real in self.acteurs_similaires:
            
            # Si un acteur similaire à 80% existe dans la base de données
            if ratio(acteur, real) > 0.8:

                # On ajoute dans les acteurs similaires proches
                close_matches.append(real)
    return close_matches


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
        """
        La fonction `form_valid` est chargée de valider et de sauvegarder un formulaire de film, y
        compris de vérifier les titres de films similaires, les acteurs similaires et les réalisateurs similaires dans la base de
        données.
        
        :param form: Le paramètre `form` est une instance d'une classe de formulaire Django. Il
        représente les données du formulaire soumises par l'utilisateur
        :return: un objet HttpResponseRedirect.
        """
        realisateur = None   
        realisateur_nom = self.request.POST.get('realisateur_nom').capitalize()
        realisateur_prenom = self.request.POST.get('realisateur_prenom').capitalize()
        force_insertion = self.request.POST.get('force-insertion-film-real') is not None
        if not force_insertion:
            form_is_invalid = False
            titre_film = self.request.POST.get('titre')
            close_matches = titre_similaire(self, titre_film)
            # Si titre similaire à celui qu'on ajoute --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("titre",f"Attention, d'autres films portent approximativement le même titre : {formatted_matches}")
                form_is_invalid = True
            
            realisateur = Realisateur.objects.filter(nom=realisateur_nom, prenom=realisateur_prenom).first()
            if realisateur is None:
                nom_prenom = f"{realisateur_nom.capitalize()} {realisateur_prenom.capitalize()}"
                close_matches = realisateur_similaire(self, nom_prenom)

                # Si réalisateur similaire à celui qu'on ajoute --> erreur
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
        """
        La fonction `form_valid` est chargée de valider et de sauvegarder un formulaire de film, y
        compris de vérifier les titres de films similaires, les acteurs similaires et les réalisateurs similaires dans la base de
        données.
        
        :param form: Le paramètre `form` est une instance d'une classe de formulaire Django. Il
        représente les données du formulaire soumises par l'utilisateur
        :return: un objet HttpResponseRedirect.
        """
        realisateur_nom = self.request.POST.get('realisateur_nom').capitalize()
        realisateur_prenom = self.request.POST.get('realisateur_prenom').capitalize()
        force_insertion = self.request.POST.get('force-insertion-film-real') is not None
        realisateur = None
        if not force_insertion:
            form_is_invalid = False
            titre_film = self.request.POST.get('titre')
            close_matches = titre_similaire(self, titre_film)

            # Si titre similaire à celui qu'on ajoute --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("titre",f"Attention, d'autres films portent approximativement le même titre : {formatted_matches}")
                form_is_invalid = True
            
            realisateur = Realisateur.objects.filter(nom=realisateur_nom, prenom=realisateur_prenom).first()
            if realisateur is None:
                nom_prenom = f"{realisateur_nom.capitalize()} {realisateur_prenom.capitalize()}"
                close_matches = realisateur_similaire(self, nom_prenom)

                # Si réalisateur similaire à celui qu'on ajoute --> erreur
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

            # Si un acteur existe dans la base de données
            if acteurs.exists():
                acteurs_similaires = [f"{realisateur.nom.capitalize()} {realisateur.prenom.capitalize()}" for realisateur in acteurs]
                for real in acteurs_similaires:
                    # Si un acteur similaire à 80% existe dans la base de données
                    if ratio(nom_prenom, real) > 0.8:
                        # On ajoute dans les acteurs similaires proches
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
        """
        La fonction `form_valid` est chargée de valider et de sauvegarder un formulaire de film, y
        compris de vérifier les réalisateurs similaires dans la base de données.
        
        :param form: Le paramètre `form` est une instance d'une classe de formulaire Django. Il
        représente les données du formulaire soumises par l'utilisateur
        :return: Le code renvoie le résultat de l'appel de la méthode `form_valid` de la classe parent
        (`super().form_valid(form)`).
        """
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = realisateur_similaire(self, nom_prenom)

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
        """
        La fonction `form_valid` vérifie si un réalisateur similaire est déjà enregistré et renvoie une
        erreur si c'est le cas.
        
        :param form: Le paramètre `form` est l'instance de formulaire en cours de validation. Il
        contient les données soumises par l'utilisateur
        :return: Le code renvoie le résultat de l'appel de la méthode `form_valid` de la classe parent
        (`super().form_valid(form)`).
        """
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = realisateur_similaire(self, nom_prenom)
            # Si c'est le cas --> erreur
            if close_matches != []:
                formatted_matches = ', '.join([s.capitalize() for s in close_matches])  # Capitaliser pour un meilleur affichage
                form.add_error("nom",f"Attention, un réalisateur similaire est déjà enregistré : {formatted_matches}")
                return self.form_invalid(form)


        return super().form_valid(form)


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
        """
        La fonction `form_valid` est chargée de valider et de sauvegarder un formulaire de film, y
        compris de vérifier les acteurs similaires dans la base de données.
        
        :param form: Le paramètre `form` est une instance d'une classe de formulaire Django. Il
        représente les données du formulaire soumises par l'utilisateur
        :return: Le code renvoie le résultat de l'appel de la méthode `form_valid` de la classe parent
        (`super().form_valid(form)`).
        """
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = acteur_similaire(self, nom_prenom)

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
        """
        La fonction `form_valid` est chargée de valider et de sauvegarder un formulaire de film, y
        compris de vérifier les acteurs similaires dans la base de données.
        
        :param form: Le paramètre `form` est une instance d'une classe de formulaire Django. Il
        représente les données du formulaire soumises par l'utilisateur
        :return: Le code renvoie le résultat de l'appel de la méthode `form_valid` de la classe parent
        (`super().form_valid(form)`).
        """
        force_insertion = self.request.POST.get('force-insertion') is not None
        if not force_insertion:
            nom = self.request.POST.get('nom').capitalize()
            prenom = self.request.POST.get('prenom').capitalize()
            nom_prenom = f"{nom.capitalize()} {prenom.capitalize()}"
            close_matches = acteur_similaire(self, nom_prenom)

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

