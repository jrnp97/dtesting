from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email, EmailValidator

# Create your models here.


class User(AbstractUser):
    """ Custom User Model """
    email = models.EmailField(
        _('email address'),
        null=False,
        blank=False,
        default=None,
        validators=[
            validate_email,
        ],
        unique=True,
    )
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            validate_email(self.email)
        except ValidationError as error:
            raise IntegrityError(error.message)
        self.slug = slugify(self.get_full_name())
        super().save(*args, **kwargs)



