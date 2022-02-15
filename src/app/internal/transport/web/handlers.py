from app.internal.services.user_service import UserService
from app.internal.transport.web.middlewares import get_only, handle_empty, parse_query_param, to_json


@get_only
@handle_empty
@to_json
@parse_query_param(["external_identifier"])
def me_info(external_identifier: str):
    user = UserService.get_user_by_external_identifier(external_identifier=external_identifier)
    return {
        "external_identifier": user.external_identifier,
        "username": user.username,
        "fullname": user.fullname,
        "phone": user.phone_number,
    }
