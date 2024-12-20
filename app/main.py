from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.captcha import router as captcha_router
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "CAPTCHA system works!"}
app.include_router(captcha_router, prefix="/captcha", tags=["Captcha"])
app.mount("/", StaticFiles(directory="static", html=True), name="static")