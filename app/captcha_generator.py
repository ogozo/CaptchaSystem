from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha():
    width, height = 200, 70
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_position = ((width - text_width) // 2, (height - text_height) // 2)

    draw.text(text_position, captcha_text, fill=(0, 0, 0), font=font)

    return image, captcha_text