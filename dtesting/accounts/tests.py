import contextlib

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.utils.text import slugify
from django.core.mail import send_mail

from unittest.mock import Mock, MagicMock, patch
from django.contrib.auth import get_user_model
from .tasks import new_login_detected
# Create your tests here.

User = get_user_model()


class TestUser(TransactionTestCase):
    """
    * Probar que el email sea unico. [OK]
    * Probar que el atributo `email` [OK], del modelo de usuario sea obligatorio.
    * Probar `first_name`, `last_name` del modelo de usuario sea obligatorio.
    * Se debe autogenerar un `slug` con el primer y segundo nombre de usuario. [OK]
    """

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


class TestLogin(TestCase):

    def test_new_login_task(self):
        """
        Testing `accounts.tasks.new_login_detected`
        signature: new_login_detected(user_id: int) -> int
        logic:
            * the task receive a parameter `user_id` and it will be an int [OK]
            * it will send an email with the `django.core.email.send_email` util. [OK] - Mock
            * the email only can be sent to the user with the `user_id`
            * [ERROR] if user_id isn't a positive int ? => it will raise a TypeError [OK].
            * [ERROR] if I don't send user_id ? => normal failure [mandatory]. [OK]
            * [ERROR] if the user_id doesn't belong to an user. => notificar a quien se logea que fallo.
            * [ERROR] if the email is not sent. => notificar a quien se logea que fallo.
                - cause 1: django's util fail.
                - cause 2: django's util return 0.
        return:
            * true if the email was sent.

        """
        # Successfully
        fake_user = User(
            username='jaime',
            password='1223456',
            email='jaime@email.com',
        )
        fake_user.save()
        # Proband que la funcion reciba el id del usuario,
        # envie el email y me retorne True cuando envia el email.
        result = new_login_detected(user_id=fake_user.id)
        self.assertTrue(result, msg="No fue enviado email, debia haber enviado por lo menos 1 email")

        # Probar que se este utilizando el django.core.mail.send_email y se este retornando ese valor.
        with patch('accounts.tasks.send_mail') as send_email_mocked:
            send_email_mocked.return_value = False
            result = new_login_detected(user_id=fake_user.id)
            self.assertEqual(send_email_mocked.call_count, 1)
            send_email_mocked.assert_called()
            self.assertFalse(result, msg="La tarea no esta retornando el valor retornado por la utilidad de django")

        print("AAA")
        # Probando que la funcion no acepte valores que no sean int y no sea negativo en el parametro `user_id`
        bad_values = [
            "1203103",
            " ",
            40505.1032,
            {},
            (1,3,4),
            -1,
            -2,
        ]
        for bad_value in bad_values:
            with self.assertRaises(TypeError):
                new_login_detected(user_id=bad_value)

        # probando que user_id sea mandatorio
        with self.assertRaisesMessage(
                TypeError,
                expected_message="new_login_detected() missing 1 required positional argument: 'user_id'",
        ):
            new_login_detected()

