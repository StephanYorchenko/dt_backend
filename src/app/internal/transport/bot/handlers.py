from telegram import Update
from telegram.ext import CallbackContext

from app.internal.services import UserService
from app.internal.transport.bot.middlewares import check_auth, prevent_errors, process_message

from .states import StatesConversation
from .types import HandlerResponse


@process_message
@prevent_errors
def start(update: Update, context: CallbackContext) -> HandlerResponse:
    UserService.create_user(
        external_identifier=update.effective_user.id,
        username=update.effective_user.username,
        fullname=" ".join([update.effective_user.first_name or "", update.effective_user.last_name or ""]),
    )
    return f"Привет, {update.effective_user.first_name}", None


@process_message
@prevent_errors
def set_up_command(update: Update, context: CallbackContext) -> HandlerResponse:
    return "Введите номер телефона", StatesConversation.PHONE_NUMBER


@process_message
@prevent_errors
def phone_handler(update: Update, context: CallbackContext) -> HandlerResponse:
    UserService.set_user_phone(external_identifier=update.effective_user.id, phone=update.message.text)
    return "Номер телефона успешно сохранён", StatesConversation.CONVERSATION_BREAK


@process_message
@prevent_errors
@check_auth
def me(update: Update, context: CallbackContext) -> HandlerResponse:
    user = UserService.get_user_by_external_identifier(external_identifier=update.effective_user.id)
    return (
        f"Имя: {user.fullname}\n"
        f"Имя пользователя: {user.username}\n"
        f"ID: {user.external_identifier}\n"
        f"Телефон: {user.phone_number}",
        None,
    )
