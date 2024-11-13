import os
from datetime import datetime
from dotenv import load_dotenv
from flask import render_template, request, jsonify
from gtts import gTTS
import pygame
import pytesseract
import cv2

from app import app

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

load_dotenv()

# Inicializando o mixer do Pygame
pygame.mixer.init()
audio_file = None


@app.route("/", methods=['GET', 'POST'])
def index():
    global audio_file

    try:
        if request.method == 'POST':
            file = request.files.get('file')

            if file and file.filename:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)

                imagem = cv2.imread(filepath)
                if imagem is None:
                    raise Exception("Erro ao ler a imagem.")

                pytesseract.pytesseract.tesseract_cmd = os.getenv("CAMINHO")
                texto = pytesseract.image_to_string(imagem, lang="por")

                # Gerar áudio do texto extraído
                tts = gTTS(text=texto, lang='pt')
                audio_file = os.path.join(app.config['UPLOAD_FOLDER'], f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
                tts.save(audio_file)

                # Carregar o áudio no Pygame
                pygame.mixer.music.load(audio_file)

                return render_template("index.html", success="Arquivo processado com sucesso!")
            else:
                return render_template("index.html", error="Nenhum arquivo foi selecionado.")
        else:
            return render_template("index.html")
    except Exception as e:
        return render_template("index.html", error=f"Erro ao processar o arquivo: {str(e)}")

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/audio/control", methods=['POST'])
def audio_control():
    global audio_file

    try:
        if not audio_file:
            return jsonify({"error": "Nenhum áudio disponível."}), 400

        data = request.json
        command = data.get("command")

        if command == "play":
            pygame.mixer.music.play()
            return jsonify({"status": "Reproduzindo"})
        elif command == "pause":
            pygame.mixer.music.pause()
            return jsonify({"status": "Pausado"})
        elif command == "unpause":
            pygame.mixer.music.unpause()
            return jsonify({"status": "Continuando"})
        elif command == "stop":
            pygame.mixer.music.stop()
            return jsonify({"status": "Parado"})
        else:
            return jsonify({"error": "Comando desconhecido."}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao controlar o áudio: {str(e)}"}), 500
