from fastapi import  HTTPException, status, Header, Depends, Request
from fastapi.security import HTTPBasic

from domain.user_session.entities import UserSession


# TODO: store credentials as .env variables
API_DOCS_CREDENTIALS = {
    "username": "username",
    "password": "password",
}

http_basic_authentication = HTTPBasic()
def authenticate_api_docs_user(
    request: Request,
    form = Depends(http_basic_authentication),
):
    if request.method == "GET":
        correct_username = form.username == API_DOCS_CREDENTIALS["username"]
        correct_password = form.password == API_DOCS_CREDENTIALS["password"]
        if not (correct_username and correct_password):
            return False
    return True


async def get_user_session_by_authorization(
    access_token: str = Header(default=None),
) -> UserSession:
    if access_token is None:
        return None
    
    access_token = access_token.replace("Bearer", "")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid authentication credentials",
        )
    
    # check is access token expired ...
    # get user session from user session cache repository ...
    user_session = UserSession(user_id=1)
    return user_session
