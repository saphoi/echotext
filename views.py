from app import app
from flask import render_template
import os
from dotenv import load_dotenv

load_dotenv()

@app.route("/")
def menuinicial():
    import pytesseract
    import cv2

    imagem = cv2.imread("testee.png")

    pytesseract.pytesseract.tesseract_cmd = os.getenv("CAMINHO")
    texto = pytesseract.image_to_string(imagem, lang="por")

    return render_template("menuinicial.html")

@app.route("/sobrenos")
def sobrenos():
    return render_template("sobrenos.html")