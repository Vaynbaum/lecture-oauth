from fastapi import Depends, FastAPI
# импортируем поток OAuth password и форму авторизации в swagger'е
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# импортируем для статических файлов
from fastapi.staticfiles import StaticFiles

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

# чтобы css (и другие статические) файлы получать
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.post("/security_enpoint")
async def action(data: dict, token: str = Depends(oauth2_scheme)):
    return {"text": f"другой {data['text']}", "token": token}
