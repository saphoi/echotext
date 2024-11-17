import os
from datetime import datetime
from dotenv import load_dotenv
from flask import render_template, request, jsonify
from gtts import gTTS
import pytesseract
import cv2
import pygame
import pytesseract
import cv2

from app import app

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Carrega as variáveis de ambiente
load_dotenv()

pygame.mixer.init()
audio_file = None

@app.route("/", methods=['GET', 'POST'])
def index():
    global audio_file

    try:
        if request.method == 'POST':
            file = request.files.get('file')

            allowed_extensions = {'png', 'jpg', 'jpeg'}
            if file and file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)

                try:
                    imagem = cv2.imread(filepath)
                    if imagem is None:
                        raise ValueError("Imagem não pôde ser lida. Verifique o formato do arquivo.")
                except cv2.error as e:
                    return render_template("index.html", error="Erro ao processar a imagem.")
                except ValueError as e:
                    return render_template("index.html", error=str(e))
                except Exception as e:
                    return render_template("index.html", error="Erro desconhecido ao carregar a imagem.")

                pytesseract.pytesseract.tesseract_cmd = os.getenv("CAMINHO")
                texto = pytesseract.image_to_string(imagem, lang="por")

                try:
                    tts = gTTS(text=texto, lang='pt')
                    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
                    tts.save(audio_file)

                    pygame.mixer.music.load(audio_file)
                except Exception as e:
                    return render_template("index.html", error=f"Erro ao gerar ou reproduzir o áudio: {str(e)}")

                return render_template("index.html", success="Arquivo processado com sucesso!")
            else:
                return render_template("index.html", error="Tipo de arquivo inválido. Envie uma imagem.")
        else:
            return render_template("index.html")
    except FileNotFoundError as e:
        return render_template("index.html", error="Arquivo não encontrado. Por favor, envie novamente.")
    except cv2.error as e:
        return render_template("index.html", error="Erro ao processar a imagem.")
    except Exception as e:
        return render_template("index.html", error="Ocorreu um erro desconhecido. Tente novamente mais tarde.")

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
