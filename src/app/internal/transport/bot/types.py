from typing import TypeAlias

from app.internal.transport.bot import states

Text: TypeAlias = str
State: TypeAlias = states.StatesConversation
HandlerResponse: TypeAlias = tuple[Text, State]
