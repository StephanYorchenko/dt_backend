import functools
import re

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from app.internal.services.user_service import UserService, GettingUserFailureException

PHONE = 1


def process_message(func):
    assert func.__annotations__["return"] == str | None

    @functools.wraps(func.__name__)
    def wrapper(update: Update, context: CallbackContext):
        text_response = func(update, context)
        if text_response is None:
            text_response = "Что-то пошло не по плану... Попробуйте ещё раз"
        update.message.reply_text(text_response)

    return wrapper


def prevent_errors(func):
    assert func.__annotations__["return"] == str, "Хэнделер сообщения должен возвращать строку"

    @functools.wraps(func.__name__)
    def wrapper(update: Update, context: CallbackContext) -> str:
        try:
            return func(update)
        except Exception:
            return None

    return wrapper


class Unauthorized(Exception):
    pass


def check_auth(func):
    assert func.__annotations__["return"] == str, "Хэнделер сообщения должен возвращать строку"

    @functools.wraps(func.__name__)
    def wrapper(update: Update, context: CallbackContext) -> str:
        try:
            user = UserService.get_user_by_external_identifier(external_identifier=update.effective_user.id)
        except GettingUserFailureException as e:
            raise Unauthorized()
        else:
            if user.phone_number:
                return func(update, context)
            raise Unauthorized()

    return wrapper


@process_message
@prevent_errors
def start(update: Update) -> str:
    UserService.create_user(
        external_identifier=update.effective_user.id,
        username=update.effective_user.username,
    )
    return f'Привет, {update.effective_user.first_name}'


@process_message
@prevent_errors
def set_command(update: Update) -> str:
    return "Введите номер телефона"


@process_message
@prevent_errors
def phone_handler(update: Update):
    UserService.set_user_phone(
        external_identifier=update.effective_user.id,
        phone=update.message
    )
    return "Номер телефона успешно сохранён"


@process_message
@prevent_errors
@check_auth
def me(update: Update, context: CallbackContext):
    user = UserService.get_user_by_external_identifier(external_identifier=update.effective_user.id)
    return "\n".join([f"{k}: {v}" for k, v in user.__dict__().items()])
