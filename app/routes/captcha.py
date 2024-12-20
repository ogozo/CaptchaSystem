from fastapi import APIRouter, Response, HTTPException
from app.captcha_generator import generate_captcha
import base64
from io import BytesIO
import secrets
from pydantic import BaseModel

router = APIRouter()
captcha_store = {}
@router.get("/generate-captcha")
def generate_captcha_endpoint():
    image, captcha_text = generate_captcha()
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    token = secrets.token_hex(16)
    captcha_store[token] = captcha_text

    return {
        "captcha_image": f"data:image/png;base64,{image_base64}",
        "token": token
    }

class CaptchaVerificationRequest(BaseModel):
    token: str
    user_input: str

@router.post("/verify-captcha")
def verify_captcha(request: CaptchaVerificationRequest):
    if request.token not in captcha_store:
        raise HTTPException(status_code=400, detail="Unvalid token")

    correct_answer = captcha_store.pop(request.token)
    if request.user_input.upper() == correct_answer:
        return {"success": True, "message": "CAPTCHA valid"}
    else:
        return {"success": False, "message": "CAPTCHA unvalid"}