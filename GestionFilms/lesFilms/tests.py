# pylint: disable=no-member

from django.test import TestCase
from .models import Film
import datetime


class FilmModelTest(TestCase):
    def setUp(self):
        self.film = Film.objects.create(
            titre="Test Film",
            description="This is a test film.",
            date_creation=datetime.date.today(),
            realisateur="Test Director",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.film), "Film Test Film de Test Director")

    def test_titre_label(self):
        field_label = self.film._meta.get_field("titre").verbose_name
        self.assertEqual(field_label, "titre")

    def test_description_label(self):
        field_label = self.film._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_date_creation_label(self):
        field_label = self.film._meta.get_field("date_creation").verbose_name
        self.assertEqual(field_label, "date creation")

    def test_realisateur_label(self):
        field_label = self.film._meta.get_field("realisateur").verbose_name
        self.assertEqual(field_label, "realisateur")

    def test_titre_max_length(self):
        max_length = self.film._meta.get_field("titre").max_length
        self.assertEqual(max_length, 250)

    def test_realisateur_max_length(self):
        max_length = self.film._meta.get_field("realisateur").max_length
        self.assertEqual(max_length, 250)

    def test_object_creation(self):
        self.assertTrue(isinstance(self.film, Film))
