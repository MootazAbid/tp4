from django.db import models


class Author(models.Model):
    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("E-mail", unique=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField("Nom", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Titre du livre", max_length=200)
    summary = models.TextField("Résumé", blank=True)
    publication_date = models.DateField("Date de publication")
    price = models.DecimalField("Prix (TND)", max_digits=8, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Auteur")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Catégorie")

    def __str__(self):
        return self.title
