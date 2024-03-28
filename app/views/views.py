from fastapi import APIRouter, Request, Form, HTTPException
from database.models import User
from database.queries import insert_or_update_user
from services.attend import login, attend
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/user")
async def add_user(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        login(email, password)
        insert_or_update_user(User(email=email, password=password))
        return templates.TemplateResponse(
            "index.html", {"request": request, "message": "User added"}
        )
    except HTTPException as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": e.detail,
                "email": email,
                "password": password,
            },
            status_code=e.status_code,
        )
