from django import forms
from django.utils import timezone
from .models import Author, Book, Category


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "summary", "publication_date", "price", "author", "category"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
            "publication_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    # Le prix doit être strictement supérieur à 0
    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Le prix doit être strictement positif.")
        return price

    # La date de publication ne doit pas être dans le futur
    def clean_publication_date(self):
        date = self.cleaned_data["publication_date"]
        if date > timezone.now().date():
            raise forms.ValidationError("La date de publication ne peut pas être dans le futur.")
        return date

    # Éviter les doublons : même titre pour le même auteur
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        author = cleaned_data.get("author")
        if title and author:
            doublons = Book.objects.filter(title__iexact=title, author=author)
            if self.instance.pk:
                doublons = doublons.exclude(pk=self.instance.pk)
            if doublons.exists():
                raise forms.ValidationError("Ce livre existe déjà pour cet auteur.")
        return cleaned_data


class AuthorForm(forms.ModelForm):
    # joined_date n'est pas dans le formulaire : auto_now_add=True la remplit
    # automatiquement à la création et le champ n'est pas modifiable (editable=False).
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "email"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
