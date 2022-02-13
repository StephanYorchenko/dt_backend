from typing import Optional

from app.internal.models import User


class UserService:
    @staticmethod
    def get_user_by_external_identifier(external_identifier: str) -> Optional[User]:
        return User.objects.filter(external_identifier=external_identifier).first()
