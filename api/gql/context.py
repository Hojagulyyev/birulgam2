from fastapi import (
    Depends,
    Request,
)

from domain.user_session.entities import UserSession

from .auth import (
    get_user_session_by_authorization,
)


async def get_context(
    request: Request,
    user_session: UserSession = Depends(
        get_user_session_by_authorization
    ),
):
    return {
        "user_session": user_session,
        "pgpool": request.state.pgpool,
    }
