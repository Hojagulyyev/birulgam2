from strawberry.types import Info

from core.errors import PermissionDeniedError
from domain.user_session.entities import UserSession


def company_required(func):
    def resolver_wrapper(info: Info, *args, **kwargs):
        user_session: UserSession = info.context["user_session"]
        if not user_session.company_id:
            raise PermissionDeniedError('user is not in the company')
        return func(info, *args, **kwargs)
    return resolver_wrapper


def user_required(func):
    def resolver_wrapper(info: Info, *args, **kwargs):
        user_session: UserSession = info.context["user_session"]
        if not user_session.user_id:
            raise PermissionDeniedError('user is not authenticated')
        return func(info, *args, **kwargs)
    return resolver_wrapper
