from typing import Annotated

from fastapi import  (
    HTTPException, 
    status, 
    Header,
    Depends, 
    Request,
    Body
)
from fastapi.security import (
    HTTPBasic, 
    HTTPAuthorizationCredentials, 
    HTTPBearer,
    HTTPBasicCredentials,
)

from domain.user_session.entities import UserSession

from adapters.token.services import TokenService
from adapters.user_session.repositories import UserSessionRedisRepository


# TODO: store credentials as .env variables
API_DOCS_CREDENTIALS = {
    "username": "username",
    "password": "password",
}


http_basic_authentication = HTTPBasic()
def authenticate_api_docs_user(
    form: HTTPBasicCredentials = Depends(http_basic_authentication),
):
    correct_username = form.username == API_DOCS_CREDENTIALS["username"]
    correct_password = form.password == API_DOCS_CREDENTIALS["password"]
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid authentication credentials"
        )


http_bearer = HTTPBearer()
async def get_user_session_by_authorization(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> UserSession | None:
    access_token: str = authorization.credentials

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid authentication credentials",
        )
    
    expired = TokenService.is_token_expired(access_token)
    if expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="access token expired",
        )
    
    user_session = await UserSessionRedisRepository().get_by_access_token(access_token)
    return user_session
