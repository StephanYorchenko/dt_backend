from abc import ABC, abstractmethod
from typing import Optional, Generic, TypeVar

User = TypeVar('User')


class UserRepository(ABC, Generic[User]):
    @abstractmethod
    def get_user_by_external_identifier(self, external_identifier: str) -> Optional[User]:
        ...

    @abstractmethod
    def create_user(self) -> Optional[User]:
        ...

    @abstractmethod
    def set_user_phone(self, external_identifier: str, phone: str) -> Optional[User]:
        ...
