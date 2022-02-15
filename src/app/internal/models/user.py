from django.core.validators import RegexValidator
from django.db.models import Model, CharField, IntegerField


class User(Model):
    external_identifier = IntegerField(
        unique=True,
        verbose_name="Telegram ID")
    username = CharField(max_length=32)
    fullname = CharField(max_length=30)
    phone_number = CharField(
        validators=[RegexValidator(regex=r"^\+?\d?\d{8,15}$")],
        max_length=16,
        blank=True
    )

    def __str__(self):
        return f'@{self.username or self.fullname}'
