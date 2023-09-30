# pylint: disable=no-member
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from lesFilms.forms import FilmForm
from lesFilms.models import Film
from django.urls import reverse


def add(request):
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
    return render(request, "lesFilms/add.html", {"form": form})


def show(request):
    films = Film.objects.all()
    return render(request, "lesFilms/show.html", {"films": films})


def edit(request, id):
    film = Film.objects.get(id=id)
    return render(request, "lesFilms/edit.html", {"film": film})


def update(request, id):
    film = Film.objects.get(id=id)
    form = FilmForm(request.POST, instance=film)
    if form.is_valid():
        form.save()
        return redirect(reverse("film_show"))
    return render(request, "lesFilms/edit.html", {"film": film})


def delete(request, id):
    film = Film.objects.get(id=id)
    film.delete()
    return redirect(reverse("film_show"))
