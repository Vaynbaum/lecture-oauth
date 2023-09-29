from fastapi import Depends, FastAPI
# испортируем встроенные способы получения ключей API
from fastapi.security import APIKeyHeader, APIKeyQuery, APIKeyCookie

app = FastAPI()

# создаем схемы получения API ключей разными способами
# (через query-параметр, заголовок, файл cookie)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_cookie = APIKeyCookie(name="auth_cookie", auto_error=False)


@app.post("/query_endpoint")
# получаем ключ api как переменную, встроенная обработка благодаря Depends(api_key_query)
async def action(data: dict, api_key: str = Depends(api_key_query)):
    # проверяем валидность ключа
    if api_key != "secret-token":
        return {"Error": "Invalid API Key"}
    return {"text": f"другой {data['text']}"}


@app.post("/header_endpoint")
# получаем ключ api как переменную, встроенная обработка благодаря Depends(api_key_header)
async def action(data: dict, api_key: str = Depends(api_key_header)):
    # проверяем валидность ключа
    if api_key != "secret-token":
        return {"Error": "Invalid API Key"}
    return {"text": f"другой {data['text']}"}


@app.post("/cookie_endpoint")
# получаем ключ api как переменную, встроенная обработка благодаря Depends(api_key_cookie)
async def action(data: dict, api_key: str = Depends(api_key_cookie)):
    # проверяем валидность ключа
    if api_key != "secret-token":
        return {"Error": "Invalid API Key"}
    return {"text": f"другой {data['text']}"}
