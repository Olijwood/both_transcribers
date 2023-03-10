from flask import Blueprint
from flask import (render_template, redirect, url_for, 
                   flash, request, Blueprint)
from flask_login import login_required
import os
import time
import whisper_audio_formatter
import deepspeech_audio_formatter
import whisper_transcriber
import deepspeech_transcriber
import ray
from threading import *

main = Blueprint('main', __name__)

APP__ROOT = os.path.dirname(os.path.abspath(__name__))
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_transcriptions():
    path_to_whisper_t = os.path.join(APP__ROOT, 'whisper_transcription/')
    for file in os.listdir(path_to_whisper_t):
        os.remove(f'{path_to_whisper_t}{file}')
    path_to_deepspeech_t = os.path.join(APP__ROOT, 'deepspeech_transcription/')
    for file in os.listdir(path_to_deepspeech_t):
        os.remove(f'{path_to_deepspeech_t}{file}')

@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("Got request in static files")
            target = os.path.join(APP__ROOT, "unformatted_audio/")

            if not os.path.isdir(target):
                os.mkdir(target)

            whisper_transcriber.delete_files()

            for file in request.files.getlist("file"):
                print(file)
                filename = file.filename
                destination = "/".join([target, filename])
                file.save(destination)

            delete_transcriptions()

            time.sleep(1)
            whisper_audio_formatter.audioFormatter()
            deepspeech_audio_formatter.main()
            
            dir_path = os.getcwd()


            def whisper_t():
                print("starting whisper")
                whisper_transcriber.main()
                whisper_transcription_path = f"{dir_path}/whisper_transcription/"
                for item in os.listdir(whisper_transcription_path):
                    if item.endswith('.txt'):
                        with open(str(whisper_transcription_path + item), "r") as f:
                            whisper_text = f.read()
                return whisper_text

            def deepspeech_t():
                deepspeech_transcriber.main()
                deepspeech_transcription_path = f'{dir_path}/deepspeech_transcription/'
                for item in os.listdir(deepspeech_transcription_path):
                    if item.endswith('.txt'):
                        with open(str(deepspeech_transcription_path + item), 'r') as g:
                            deepspeech_text = g.read()
                return deepspeech_text

            t1 = Thread(target=whisper_t)
            t2 = Thread(target=deepspeech_t)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            return redirect(url_for('transcripts.transcriptions', f_name=filename))
    return render_template("index2.html")

@main.route("/about")
def about():
    return render_template("about.html")
