from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from .models import Author, Book, Category
from .forms import BookForm


class CatalogueTests(TestCase):
    def setUp(self):
        self.a = Author.objects.create(first_name="Tahar", last_name="Ben Jelloun", email="t@x.tn")
        self.c = Category.objects.create(name="Roman")
        self.b = Book.objects.create(title="L'Enfant de sable", publication_date=date(1985, 1, 1),
                                     price=35, author=self.a, category=self.c)

    def data(self, **kw):
        d = {"title": "Nouveau", "summary": "", "publication_date": "2000-01-01",
             "price": "20", "author": self.a.pk, "category": self.c.pk}
        d.update(kw)
        return d

    def test_form_vide(self):
        self.assertEqual(self.client.get(reverse("catalogue:livre_create")).status_code, 200)

    def test_creation_valide(self):
        r = self.client.post(reverse("catalogue:livre_create"), self.data(), follow=True)
        self.assertContains(r, "a été ajouté")

    def test_prix_negatif(self):
        r = self.client.post(reverse("catalogue:livre_create"), self.data(price="-5"))
        self.assertContains(r, "Le prix doit être strictement positif.")

    def test_date_futur(self):
        f = (date.today() + timedelta(days=30)).isoformat()
        r = self.client.post(reverse("catalogue:livre_create"), self.data(publication_date=f))
        self.assertContains(r, "dans le futur")

    def test_doublon_livre(self):
        r = self.client.post(reverse("catalogue:livre_create"), self.data(title="L'Enfant de sable"))
        self.assertContains(r, "existe déjà")

    def test_email_unique(self):
        r = self.client.post(reverse("catalogue:auteur_create"),
                             {"first_name": "A", "last_name": "B", "email": "t@x.tn"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Author.objects.count(), 1)

    def test_modification_prerempli(self):
        r = self.client.get(reverse("catalogue:livre_update", args=[self.b.pk]))
        self.assertContains(r, 'value="1985-01-01"')

    def test_suppression(self):
        url = reverse("catalogue:livre_delete", args=[self.b.pk])
        self.assertContains(self.client.get(url), "Confirmer la suppression")
        self.assertEqual(Book.objects.count(), 1)  # GET ne supprime pas
        r = self.client.post(url, follow=True)
        self.assertContains(r, "a été supprimé")
        self.assertEqual(Book.objects.count(), 0)

    def test_recherche(self):
        r = self.client.get(reverse("catalogue:livre_list") + "?q=sable")
        self.assertContains(r, "L&#x27;Enfant de sable")
        self.assertContains(r, 'value="sable"')
        r = self.client.get(reverse("catalogue:livre_list") + "?q=zzz")
        self.assertContains(r, "Aucun livre trouvé")

    def test_auteur_modif_et_suppression_cascade(self):
        r = self.client.post(reverse("catalogue:auteur_update", args=[self.a.pk]),
                             {"first_name": "Tahar", "last_name": "BJ", "email": "t@x.tn"})
        self.assertEqual(r.status_code, 302)
        r = self.client.get(reverse("catalogue:auteur_delete", args=[self.a.pk]))
        self.assertContains(r, "1 livre")
        self.client.post(reverse("catalogue:auteur_delete", args=[self.a.pk]))
        self.assertEqual(Book.objects.count(), 0)

    def test_categorie_protegee(self):
        r = self.client.post(reverse("catalogue:categorie_delete", args=[self.c.pk]), follow=True)
        self.assertContains(r, "Impossible de supprimer")
        self.assertTrue(Category.objects.filter(pk=self.c.pk).exists())

    def test_categorie_create_et_delete_vide(self):
        self.client.post(reverse("catalogue:categorie_create"), {"name": "Poésie"})
        c = Category.objects.get(name="Poésie")
        self.client.post(reverse("catalogue:categorie_delete", args=[c.pk]))
        self.assertFalse(Category.objects.filter(name="Poésie").exists())

    def test_csrf(self):
        from django.test import Client
        r = Client(enforce_csrf_checks=True).post(reverse("catalogue:livre_create"), self.data())
        self.assertEqual(r.status_code, 403)
