const captchaImage = document.getElementById("captcha-image");
const refreshCaptchaButton = document.getElementById("refresh-captcha");
const submitCaptchaButton = document.getElementById("submit-captcha");
const captchaInput = document.getElementById("captcha-input");
const resultMessage = document.getElementById("result-message");

let currentToken = "";
const refreshCaptcha = async () => {
    try {
        const response = await fetch("/captcha/generate-captcha");
        const data = await response.json();
        captchaImage.src = data.captcha_image;
        currentToken = data.token;
    } catch (error) {
        console.error("CAPTCHA yenileme hatası:", error);
    }
};

const submitCaptcha = async () => {
    const userInput = captchaInput.value;
    if (!userInput) {
        resultMessage.textContent = "Lütfen CAPTCHA'yı girin.";
        resultMessage.style.color = "red";
        return;
    }

    try {
        const response = await fetch("/captcha/verify-captcha", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                token: currentToken,
                user_input: userInput,
            }),
        });

        const data = await response.json();
        if (data.success) {
            resultMessage.textContent = "CAPTCHA doğrulandı!";
            resultMessage.style.color = "green";
        } else {
            resultMessage.textContent = "CAPTCHA yanlış, tekrar deneyin.";
            resultMessage.style.color = "red";
        }
    } catch (error) {
        console.error("CAPTCHA doğrulama hatası:", error);
        resultMessage.textContent = "Bir hata oluştu, tekrar deneyin.";
        resultMessage.style.color = "red";
    }
};

refreshCaptchaButton.addEventListener("click", refreshCaptcha);
submitCaptchaButton.addEventListener("click", submitCaptcha);

refreshCaptcha();