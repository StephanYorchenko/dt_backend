import functools
from typing import List

from django.http import HttpResponse, JsonResponse

from app.internal.services.user_service import UserService


def get_only(func):
    @functools.wraps(func.__name__)
    def wrapper(request):
        if request.method == 'GET':
            return func(request)
        return HttpResponse(f"Not right type of response", status=405)

    return wrapper


def handle_empty(func):
    @functools.wraps(func.__name__)
    def wrapper(request):
        response = func(request)
        if response is not None:
            return func(request)
        return HttpResponse(f'Does not exist', status=403)

    return wrapper


def to_json(func):
    @functools.wraps(func.__name__)
    def wrapper(request):
        response = func(request)
        if response is not None:
            return JsonResponse(data=response.__dict__(), status=200)

    return wrapper


def parse_query_param(param_names: List[str]):
    def decorator(func):
        @functools.wraps(func.__name__)
        def wrapper(request):
            kwargs = {param_name: request.GET.get(param_name) for param_name in param_names}
            return func(**kwargs)

        return wrapper

    return decorator


@get_only
@handle_empty
@to_json
@parse_query_param(["external_identifier"])
def me_info(external_identifier: str):

    return UserService.get_user_by_external_identifier(external_identifier=external_identifier)
