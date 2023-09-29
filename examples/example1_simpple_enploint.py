# испортируем класс FastAPI
from fastapi import FastAPI

# создаем приложение FastAPI
app = FastAPI() 


# через декоратор создаем endpoint (метод)
@app.post("/endpoint")
# метод принимает dict (json)
async def action(data: dict):
    # метод возвращает dict, который будет как json
    return {"text": f"другой {data['text']}"}
