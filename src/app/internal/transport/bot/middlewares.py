import functools

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from app.internal.services import UserService
from app.internal.services.user_service import GettingUserFailureException

from .states import StatesConversation
from .types import HandlerResponse


def process_message(func):
    @functools.wraps(func.__name__)
    def wrapper(update: Update, context: CallbackContext):
        text_response, state = func(update, context)
        if text_response is None and state is None:
            text_response = "Что-то пошло не по плану... Попробуйте ещё раз"
        update.message.reply_text(text_response)
        if state is not None:
            return ConversationHandler.END if state == StatesConversation.CONVERSATION_BREAK else state

    return wrapper


def prevent_errors(func):
    @functools.wraps(func.__name__)
    def wrapper(update: Update, context: CallbackContext) -> HandlerResponse | None:
        try:
            return func(update, context)
        except Exception:
            return None, None

    return wrapper


class Unauthorized(Exception):
    pass


def check_auth(func):
    @functools.wraps(func.__name__)
    def wrapper(update: Update, context: CallbackContext) -> HandlerResponse:
        try:
            user = UserService.get_user_by_external_identifier(external_identifier=update.effective_user.id)
        except GettingUserFailureException:
            raise Unauthorized()
        else:
            if user.phone_number:
                return func(update, context)
            return "Вы не указали свой номер телефона", None

    return wrapper
