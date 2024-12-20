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
        console.error("CAPTCHA renew error:", error);
    }
};

const submitCaptcha = async () => {
    const userInput = captchaInput.value;
    if (!userInput) {
        resultMessage.textContent = "Please enter the CAPTCHA.";
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
            resultMessage.textContent = "CAPTCHA is verified!";
            resultMessage.style.color = "green";
        } else {
            resultMessage.textContent = "CAPTCHA is wrong, try again.";
            resultMessage.style.color = "red";
        }
    } catch (error) {
        console.error("CAPTCHA verifying error:", error);
        resultMessage.textContent = "An error occured, try again.";
        resultMessage.style.color = "red";
    }
};

refreshCaptchaButton.addEventListener("click", refreshCaptcha);
submitCaptchaButton.addEventListener("click", submitCaptcha);

refreshCaptcha();