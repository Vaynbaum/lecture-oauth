from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse

CLIENT_ID = "235694458387-3rni6dlbi635e1ghgr72in281u0d8tu7.apps.googleusercontent.com"
CLIENT_SECRET = "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"
SECRET_KEY = "cTlpQmB8MbDtsf6wzOQi0P2rfwEXy3sBD49wCn5I"

config_data = {"GOOGLE_CLIENT_ID": CLIENT_ID, "GOOGLE_CLIENT_SECRET": CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "email profile openid"},
)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.get("/")
def public(request: Request):
    user = request.session.get("user")
    if user:
        name = user.get("name")
        return HTMLResponse(f"<p>Hello {name}!</p><a href=/logout>Logout</a>")
    return HTMLResponse("<a href=/login>Login</a>")


@app.route("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


@app.route("/login")
async def login(request: Request):
    redirect_uri = request.url_for(
        "auth"
    )  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url="/")
    user_data = await oauth.google.parse_id_token(access_token, None)
    request.session["user"] = dict(user_data)
    return RedirectResponse(url="/")
