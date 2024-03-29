from fastapi import APIRouter, Request, Form, HTTPException
from database.models import User
from database import queries
from services import attend
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/user")
async def add_user(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        driver = attend.login(email, password)
        cookies = attend.login_lk(email, password, driver)
        queries.insert_or_update_cookies(cookies, email)
        queries.insert_or_update_user(User(email=email, password=password))
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
