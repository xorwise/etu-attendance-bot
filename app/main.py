from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from database.queries import create_table
from views.views import router
from dotenv import load_dotenv

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)


if __name__ == "__main__":
    load_dotenv(".env")
    create_table()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
