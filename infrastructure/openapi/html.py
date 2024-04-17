import json
from typing import Any, Dict, Optional

from fastapi.openapi.docs import swagger_ui_default_parameters
from fastapi.encoders import jsonable_encoder
from starlette.responses import HTMLResponse
from typing_extensions import Annotated, Doc


def get_swagger_ui_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that Swagger UI should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    swagger_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
    swagger_css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI CSS.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    swagger_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Annotated[
        Optional[str],
        Doc(
            """
            The OAuth2 redirect URL, it is normally automatically handled by FastAPI.
            """
        ),
    ] = None,
    init_oauth: Annotated[
        Optional[Dict[str, Any]],
        Doc(
            """
            A dictionary with Swagger UI OAuth2 initialization configurations.
            """
        ),
    ] = None,
    swagger_ui_parameters: Annotated[
        Optional[Dict[str, Any]],
        Doc(
            """
            Configuration parameters for Swagger UI.

            It defaults to [swagger_ui_default_parameters][fastapi.openapi.docs.swagger_ui_default_parameters].
            """
        ),
    ] = None,
    shard: str = "primary",
    signin_url: str,
    username: str,
    password: str,
) -> HTMLResponse:
    """
    Generate and return the HTML  that loads Swagger UI for the interactive
    API docs (normally served at `/docs`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load Swagger UI's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)
    and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    # Custom Code

    html += f"""
    const signinUrl = '{signin_url}';
    const shard = '{shard}';
    """
    html += "const signinBody = {username: '" + username + "', password: '" + password + "'};"
    html += f"""
        let accessToken;
        """

    html += """
    
    window.onload = function() {
        setTimeout(() => {
            const authSignInSection = document.getElementById("operations-auth-signin_user_route_auth_signin_post");
            authSignInSection.style.backgroundColor = "#eee5fb";
            
            fetch(`${signinUrl}`, {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    "shard": `${shard}`
                  },
                  body: JSON.stringify(signinBody)
                })
                .then(response => response.json()) // Parse the response as JSON
                .then(data => {
                    accessToken = data;
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                });
        
            const authButton = document.querySelector(".unlocked");
            authButton.addEventListener("click", () => {
                setTimeout(() => {
                    const authInput = document.querySelector('[aria-label="auth-bearer-value"]');
                    authInput.value = accessToken;
                    authInput.focus();
                }, 100);
            });
            
            window.addEventListener('keydown', (event) => {
                const authButton = document.querySelector(".unlocked");
                const closeButton = document.querySelector(".close-modal");
                if (event.key === 'Shift' && authButton) {
                    authButton.click();
                }
                else if (event.key === 'Shift' && closeButton) {
                    closeButton.click();
                }
            });
            
        }, 100)
    };
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
