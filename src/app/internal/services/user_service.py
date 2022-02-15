import functools
import re
from typing import Optional, Type

from app.internal.models import User


class CreationFailureException(Exception):
    message = "Ошибка создания пользователя"


class GettingUserFailureException(Exception):
    message = "Ошибка получения пользователя"


class UpdatingUserFailureException(Exception):
    pass


class NotFoundException(Exception):
    message = "Не найден пользователь"


def raises(exception: Type[Exception]):
    def decorator(func):
        @functools.wraps(func.__name__)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception() from e

        return wrapper

    return decorator


class UserService:
    @staticmethod
    @raises(GettingUserFailureException)
    def get_user_by_external_identifier(external_identifier: str) -> Optional[User]:
        if not (user := User.objects.filter(external_identifier=external_identifier).first()):
            raise NotFoundException()
        return user

    @staticmethod
    @raises(CreationFailureException)
    def create_user(external_identifier: str, username: str, fullname: str) -> None:
        User.objects.get_or_create(
                external_identifier=external_identifier,
                username=username,
                fullname=fullname
        )

    @staticmethod
    @raises(UpdatingUserFailureException)
    def set_user_phone(external_identifier: str, phone: str) -> None:
        if not (user := User.objects.filter(external_identifier=external_identifier).first()):
            raise NotFoundException()
        if re.match(r"^\+?\d?\d{8,15}$", phone):
            user.phone_number = phone
            user.save()
        else:
            raise UpdatingUserFailureException()
