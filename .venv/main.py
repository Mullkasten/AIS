import uvicorn
from fastapi import FastAPI
from application.routes import router


app = FastAPI()


app.include_router(router)      # подключаем обработчик API URI

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
