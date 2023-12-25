import uvicorn
from fastapi import FastAPI
from application.routes import router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://192.168.56.104"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # здесь указываем разрешённые адреса, символ "*"разрешает запросы для всех адресов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)      # подключаем обработчик API URI

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
