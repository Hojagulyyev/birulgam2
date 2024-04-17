from fastapi import (
    FastAPI, 
    APIRouter,
    Depends,
)

from infrastructure.fastapi.config import APP_CONFIG
from infrastructure.openapi.html import get_swagger_ui_html
from api.http.auth import authenticate_api_docs_user

from . import VERSION
from . import (
    product,
)


router = APIRouter()
router.include_router(product.router)

app = FastAPI(**APP_CONFIG)
app.include_router(router)


@app.get(
    path="/docs",
    dependencies=[
        Depends(authenticate_api_docs_user),
    ],
    include_in_schema=False,
)
async def get_api_docs():
    return get_swagger_ui_html(
        openapi_url=f"/api/{VERSION}/openapi.json",
        title="Python Clean Architecture",
        shard="DEFAULT_SHARD_NAME",
        signin_url="{BASE_URL}/api/{VERSION}/auth/signin/",
        username="DEFAULT_USER_USERNAME_FOR_OPENAPI_ROUTES",
        password="DEFAULT_USER_PASSWORD_FOR_OPENAPI_ROUTES",
    )
