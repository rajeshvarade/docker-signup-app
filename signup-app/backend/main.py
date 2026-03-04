from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from passlib.context import CryptContext
import itsdangerous
import os

app = FastAPI()

# FRONTEND PATH
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Serve static files (css, js, images)
app.mount("/static", StaticFiles(directory=f"{FRONTEND_PATH}"), name="static")

# Jinja2 templates (HTML files)
templates = Jinja2Templates(directory=FRONTEND_PATH)

# Password hashing

# In-memory DB
users_db = {}

# Cookie signer
secret_key = "your-secret-key"
serializer = itsdangerous.URLSafeSerializer(secret_key)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = None
    cookie = request.cookies.get("session")

    if cookie:
        try:
            user = serializer.loads(cookie)
        except Exception:
            pass

    return templates.TemplateResponse("welcome.html", {"request": request, "user": user})


@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...)):
    if username in users_db:
        return HTMLResponse("User already exists")

  
    users_db[username] = username

    return RedirectResponse("/signin", status_code=302)


@app.get("/signin", response_class=HTMLResponse)
def signin_form(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@app.post("/signin")
def signin(response: Response, username: str = Form(...), password: str = Form(...)):
    if username not in users_db:
        return HTMLResponse("Invalid username or password")

    hashed = users_db[username]
    
    # Create session cookie
    token = serializer.dumps(username)
    response = RedirectResponse("/", status_code=302)
    response.set_cookie("session", token)

    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("session")
    return response