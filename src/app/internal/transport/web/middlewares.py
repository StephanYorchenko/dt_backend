import functools
from typing import List

from django.http import HttpResponse, JsonResponse


def get_only(func):
    @functools.wraps(func.__name__)
    def wrapper(request):
        if request.method == "GET":
            return func(request)
        return HttpResponse("Not right type of response", status=405)

    return wrapper


def handle_empty(func):
    @functools.wraps(func.__name__)
    def wrapper(request):
        response = func(request)
        if response is not None:
            return func(request)
        return HttpResponse("Does not exist", status=403)

    return wrapper


def to_json(func):
    @functools.wraps(func.__name__)
    def wrapper(request):
        response = func(request)
        if response is not None:
            return JsonResponse(data=response, status=200)

    return wrapper


def parse_query_param(param_names: List[str]):
    def decorator(func):
        @functools.wraps(func.__name__)
        def wrapper(request):
            kwargs = {param_name: request.GET.get(param_name) for param_name in param_names}
            return func(**kwargs)

        return wrapper

    return decorator
