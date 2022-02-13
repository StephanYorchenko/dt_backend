from app.internal.services.user_service import UserService

from app.internal.transport.middlewares import get_only, handle_empty, to_json, parse_query_param


@get_only
@handle_empty
@to_json
@parse_query_param(["external_identifier"])
def me_info(external_identifier: str):
    return UserService.get_user_by_external_identifier(external_identifier=external_identifier)
