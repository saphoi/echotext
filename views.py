# padrão
import os
from datetime import datetime

# terceiros
from dotenv import load_dotenv
from flask import render_template, request
from gtts import gTTS
import pytesseract
import cv2
import pygame

# locais
from app import app

# config iniciais
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Carrega as variáveis de ambiente
load_dotenv()
print("CAMINHO:", os.getenv("CAMINHO"))
print("TESSDATA_PREFIX:", os.getenv("TESSDATA_PREFIX"))



# Função pra processar a imagem
def process_image(file_path):
    # Carrega a imagem e extrai o texto
    imagem = cv2.imread(file_path)
    # Converte a imagem de BGR (OpenCV) para RGB (PIL/Tesseract)
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = os.getenv("CAMINHO")
    os.environ['TESSDATA_PREFIX'] = os.getenv("TESSDATA_PREFIX")
    #print(f"Caminho do Tesseract: {pytesseract.pytesseract.tesseract_cmd}")
    texto = pytesseract.image_to_string(imagem_rgb, lang="por")
    return texto

# Função para converter texto em áudio
def text_to_speech(text):
    # Gera o arquivo de áudio usando gTTS
    tts = gTTS(text=text, lang='pt')
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
    tts.save(audio_file)
    return audio_file

# Função para tocar o áudio
def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

# Rota principal
@app.route("/", endpoint='index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename:
            # Salva o arquivo
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Processa a imagem e converte o texto em áudio
            texto = process_image(filepath)
            audio_file = text_to_speech(texto)

            # Reproduz o áudio
            play_audio(audio_file)

            return render_template("index.html")
        else:
            return render_template("index.html", error="Nenhum arquivo foi selecionado")
    else:
        return render_template("index.html")


# Rota 'sobre nós'
@app.route("/about")
def about():
    return render_template("about.html")
