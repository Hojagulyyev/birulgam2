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
    HTTPBasicCredentials,
)
import jwt

from domain.user_session.entities import UserSession

from adapters.token.services import TokenService
from adapters.user_session.repositories import UserSessionRedisRepository


# TODO: store credentials as .env variables
API_DOCS_CREDENTIALS = {
    "username": "username",
    "password": "password",
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
    request: Request,
    access_token: str = Header(None),
    body = Body(None),
) -> UserSession | None:
    if body is None:
        return None
    
    authorization = access_token
    if not authorization:
        if (
            request.method == "POST"
            and "IntrospectionQuery" not in body["query"]
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid authentication credentials",
            )
        # do nothing when GraphiQL opened
        # do nothing when GraphiQL Docs generated
        else:
            return None
    
    access_token = authorization.replace("Bearer ", "")
    try:
        expired = TokenService.is_token_expired(access_token)
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid access token",
        )

    if expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="access token expired",
        )
    
    user_session = await UserSessionRedisRepository().get_by_access_token(access_token)
    return user_session
