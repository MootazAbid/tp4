from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    # Livres
    path("livres/", views.livre_list, name="livre_list"),
    path("livres/ajouter/", views.livre_create, name="livre_create"),
    path("livres/<int:pk>/", views.livre_detail, name="livre_detail"),
    path("livres/<int:id>/modifier/", views.livre_update, name="livre_update"),
    path("livres/<int:id>/supprimer/", views.livre_delete, name="livre_delete"),
    # Auteurs
    path("auteurs/", views.auteur_list, name="auteur_list"),
    path("auteurs/ajouter/", views.auteur_create, name="auteur_create"),
    path("auteurs/<int:pk>/", views.auteur_detail, name="auteur_detail"),
    path("auteurs/<int:id>/modifier/", views.auteur_update, name="auteur_update"),
    path("auteurs/<int:id>/supprimer/", views.auteur_delete, name="auteur_delete"),
    # Catégories
    path("categories/", views.categorie_list, name="categorie_list"),
    path("categories/ajouter/", views.categorie_create, name="categorie_create"),
    path("categories/<int:id>/supprimer/", views.categorie_delete, name="categorie_delete"),
]
