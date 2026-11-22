from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect

from .forms import BookForm, AuthorForm, CategoryForm
from .models import Author, Book, Category


# ---------- Consultation (Atelier 03) + recherche (Partie 6) ----------
def livre_list(request):
    q = request.GET.get("q", "").strip()
    livres = Book.objects.select_related("author", "category")
    if q:
        livres = livres.filter(title__icontains=q)
    return render(request, "catalogue/livre_list.html", {"livres": livres, "q": q})


def livre_detail(request, pk):
    livre = get_object_or_404(Book, pk=pk)
    return render(request, "catalogue/livre_detail.html", {"livre": livre})


def auteur_list(request):
    return render(request, "catalogue/auteur_list.html", {"auteurs": Author.objects.all()})


def auteur_detail(request, pk):
    auteur = get_object_or_404(Author, pk=pk)
    return render(request, "catalogue/auteur_detail.html",
                  {"auteur": auteur, "livres": auteur.book_set.all()})


def categorie_list(request):
    return render(request, "catalogue/categorie_list.html", {"categories": Category.objects.all()})


# ---------- Livres : créer / modifier / supprimer ----------
def livre_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            livre = form.save()
            messages.success(request, f"Le livre « {livre.title} » a été ajouté.")
            return redirect("catalogue:livre_detail", pk=livre.pk)
    else:
        form = BookForm()
    context = {"form": form, "titre_page": "Ajouter un livre"}
    return render(request, "catalogue/livre_form.html", context)


def livre_update(request, id):
    livre = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, "Le livre a été modifié.")
            return redirect("catalogue:livre_detail", pk=livre.pk)
    else:
        form = BookForm(instance=livre)
    context = {"form": form, "titre_page": f"Modifier : {livre.title}"}
    return render(request, "catalogue/livre_form.html", context)


def livre_delete(request, id):
    livre = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        titre = livre.title
        livre.delete()
        messages.success(request, f"Le livre « {titre} » a été supprimé.")
        return redirect("catalogue:livre_list")
    return render(request, "catalogue/livre_confirm_delete.html", {"livre": livre})


# ---------- Auteurs : créer / modifier / supprimer ----------
def auteur_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            auteur = form.save()
            messages.success(request, f"L'auteur « {auteur} » a été ajouté.")
            return redirect("catalogue:auteur_detail", pk=auteur.pk)
    else:
        form = AuthorForm()
    context = {"form": form, "titre_page": "Ajouter un auteur"}
    return render(request, "catalogue/auteur_form.html", context)


def auteur_update(request, id):
    auteur = get_object_or_404(Author, pk=id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=auteur)
        if form.is_valid():
            form.save()
            messages.success(request, "L'auteur a été modifié.")
            return redirect("catalogue:auteur_detail", pk=auteur.pk)
    else:
        form = AuthorForm(instance=auteur)
    context = {"form": form, "titre_page": f"Modifier : {auteur}"}
    return render(request, "catalogue/auteur_form.html", context)


def auteur_delete(request, id):
    auteur = get_object_or_404(Author, pk=id)
    nb_livres = auteur.book_set.count()  # livres supprimés en cascade
    if request.method == "POST":
        nom = str(auteur)
        auteur.delete()
        messages.success(request, f"L'auteur « {nom} » a été supprimé.")
        return redirect("catalogue:auteur_list")
    context = {"auteur": auteur, "nb_livres": nb_livres}
    return render(request, "catalogue/auteur_confirm_delete.html", context)


# ---------- Catégories : créer / supprimer ----------
def categorie_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            categorie = form.save()
            messages.success(request, f"La catégorie « {categorie.name} » a été ajoutée.")
            return redirect("catalogue:categorie_list")
    else:
        form = CategoryForm()
    context = {"form": form, "titre_page": "Ajouter une catégorie"}
    return render(request, "catalogue/categorie_form.html", context)


def categorie_delete(request, id):
    categorie = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        try:
            nom = categorie.name
            categorie.delete()
            messages.success(request, f"La catégorie « {nom} » a été supprimée.")
        except ProtectedError:
            messages.error(request, "Impossible de supprimer cette catégorie : elle contient des livres.")
        return redirect("catalogue:categorie_list")
    return render(request, "catalogue/categorie_confirm_delete.html", {"categorie": categorie})
