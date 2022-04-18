from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.utils.text import slugify

from .models import User
# Create your tests here.

"""
* Probar que el email sea unico. [OK]
* Probar que el atributo `email` [OK], del modelo de usuario sea obligatorio.
* Probar `first_name`, `last_name` del modelo de usuario sea obligatorio.
* Se debe autogenerar un `slug` con el primer y segundo nombre de usuario. [OK]
"""


class TestUser(TransactionTestCase):

    def test_slug_autogeneration(self):
        """ """
        user = User(
            username='jaime',
            password='123456',
            email='mimosa@gmail.com',
            first_name='Jaime',
            last_name='Negrete',
        )
        expected_slug = slugify(user.get_full_name())
        user.save()
        db_user = User.objects.get(email=user.email)
        self.assertEqual(db_user.slug, expected_slug)

    def test_user_email_unique(self):
        """"""
        user = User(
            username='jaime',
            password='123456',
            email='mimosa@gmail.com',
        )
        user.save()
        user_two = User(
            username='maria',
            password='123456',
            email='mimosa@gmail.com',
        )
        with self.assertRaisesMessage(IntegrityError, expected_message='UNIQUE constraint failed: accounts_user.email'):
            user_two.save()

    def test_user_email_mandatory(self):
        """
        Testing `accounts.User` model has the `email` column as not-null
        """
        user = User(
            username='jaime',
            password='123456',
        )
        with self.assertRaises(IntegrityError):
            user.save()
        bad_values = [
            '',
            '    ',
            '@masfaf',
            'jaime@',
            'mimosa',
        ]
        for bad_val in bad_values:
            user.email = bad_val
            with self.assertRaises(IntegrityError, msg=f"Invalid validation for value {bad_val}"):
                user.save()  # Guardando el modelo.

        user.email = 'mimosa@gmail.com'
        user.save()
        db_user = User.objects.get(email=user.email)
        self.assertEqual(user.id, db_user.id)

