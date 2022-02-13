from django.db.models import Model, PositiveBigIntegerField, CharField
from django.core.validators import RegexValidator


class User(Model):
    external_identifier = PositiveBigIntegerField(primary_key=True)
    username = CharField(max_length=32)
    fullname = CharField(max_length=30)
    phoneNumberRegex = RegexValidator(regex=r"^\+?\d?\d{8,15}$")
    phoneNumber = CharField(validators=[phoneNumberRegex], max_length=16, unique=True)

    def __str__(self):
        return f'@{self.username or self.fullname}'

    def __dict__(self):
        return {
            "external_identifier": self.external_identifier,
            "username": self.username,
            "fullname": self.fullname,
            "phone": self.phoneNumber
        }
