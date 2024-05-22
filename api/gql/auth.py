from fastapi import  (
    HTTPException, 
    status, 
    Header,
    Depends, 
    Request,
)
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)
import jwt

from core.errors import PermissionDeniedError
from domain.user_session.entities import UserSession

from adapters.token.services import TokenService
from adapters.user_session.repositories import UserSessionRedisRepository

from infrastructure import env


API_DOCS_CREDENTIALS = {
    "username": env.USERNAME_FOR_GRAPHIQL,
    "password": env.PASSWORD_FOR_GRAPHIQL,
}

security = HTTPBasic()
def authenticate_api_docs_user(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if request.method == "GET":
        correct_username = credentials.username == API_DOCS_CREDENTIALS["username"]
        correct_password = credentials.password == API_DOCS_CREDENTIALS["password"]
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid authentication credentials"
            )

# TODO: add docs security by authenticate_api_docs_user function
async def get_user_session_by_authorization(
    access_token: str = Header(None),
) -> UserSession:
    authorization = access_token
    user_session_repo = UserSessionRedisRepository()
    
    if not authorization:
        user_session = await user_session_repo.make_empty()
        return user_session
    
    access_token = authorization.replace("Bearer ", "")
    try:
        expired = TokenService.is_token_expired(access_token)
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                PermissionDeniedError(
                    msg='invalid access token',
                ).serialize()
            ),
        )

    if expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                PermissionDeniedError(
                    msg='access token expired',
                ).serialize()
            ),
        )
    
    user_session = await user_session_repo.get_by_access_token(access_token)
    return user_session
