from app import app
from flask import render_template, request
import os
from dotenv import load_dotenv
from gtts import gTTS
import pygame
from PIL import Image

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

load_dotenv()

@app.route("/", endpoint='index', methods=['GET', 'POST'])
def index():
    import pytesseract
    import cv2
    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            imagem = cv2.imread(filepath)

            pytesseract.pytesseract.tesseract_cmd = os.getenv("CAMINHO")
            texto = pytesseract.image_to_string(imagem, lang="por")

            tts = gTTS(text=texto, lang='pt')
            audio_file = "audio.mp3"  
            tts.save(audio_file)  

            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            return render_template("index.html")
        else:
             return render_template("index.html", error="Nenhum arquivo foi selecionado")
    else:
        return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
