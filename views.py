from app import app
from flask import render_template
import os
from dotenv import load_dotenv
from gtts import gTTS
import pygame

load_dotenv()

@app.route("/", endpoint='index')
def index():
    import pytesseract
    import cv2

    imagem = cv2.imread("testee.png")

    pytesseract.pytesseract.tesseract_cmd = os.getenv("CAMINHO")
    texto = pytesseract.image_to_string(imagem, lang="por")

    tts = gTTS(text=texto, lang='pt')
    audio_file = "audio.mp3"  
    tts.save(audio_file)  

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    #os.system("start audio.mp3")

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
