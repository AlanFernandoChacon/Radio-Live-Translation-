#!/usr/bin/env python3
import os
import time
import subprocess
import threading
import openai
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
from datetime import datetime
from queue import Queue

# Cargar API Key desde .env
load_dotenv()
openai.api_key = YOUR API KEY
# Configuración
RADIO_URL = "https://live-icy.dr.dk/A/A03H.mp3"
BLOCK_DURATION = 60  # segundos
LANGUAGE = "da"

AUDIO_FOLDER = "audio_blocks"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

console = Console()
bloque_nro = 1
cola_bloques = Queue()


def grabar_y_transcribir():
    global bloque_nro
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        audio_file = os.path.join(AUDIO_FOLDER, f"bloque_{bloque_nro}.wav")

        console.print(f"[yellow]🎙️ Grabando bloque #{bloque_nro}...[/yellow]")
        subprocess.run([
            "ffmpeg", "-y", "-i", RADIO_URL, "-t", str(BLOCK_DURATION),
            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            with open(audio_file, "rb") as f:
                response = openai.audio.transcriptions.create(
                    file=f,
                    model="whisper-1",
                    language=LANGUAGE
                )
                texto_da = response.text
        except Exception as e:
            texto_da = f"[ERROR de transcripción]: {e}"

        texto_es = traducir_con_openai(texto_da, "es")
        texto_en = traducir_con_openai(texto_da, "en")

        cola_bloques.put((timestamp, audio_file, texto_da, texto_es, texto_en))
        bloque_nro += 1
        time.sleep(1)


def reproducir_y_mostrar():
    while True:
        if not cola_bloques.empty():
            timestamp, audio_file, texto_da, texto_es, texto_en = cola_bloques.get()

            console.rule(f"[bold green]🎧 [{timestamp}] Bloque")
            console.print(Panel.fit(texto_da, title="🇩🇰 Danés", padding=(1, 2), style="yellow"))
            console.print(Panel.fit(texto_es, title="🇪🇸 Español", padding=(1, 2), style="blue"))
            console.print(Panel.fit(texto_en, title="🇺🇸 Inglés", padding=(1, 2), style="magenta"))

            guardar_en_archivo(timestamp, texto_da, texto_es, texto_en)

            console.print("[green]▶️ Reproduciendo bloque grabado...[/green]")
            subprocess.run([
                "ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio_file
            ])
        else:
            time.sleep(0.5)


def traducir_con_openai(texto, idioma_destino):
    prompts = {
        "es": f"Traducí esto del danés al español, sin explicaciones:\n\"{texto}\"",
        "en": f"Translate this from Danish to English, no explanation:\n\"{texto}\""
    }
    try:
        respuesta = openai.chat.completions.create(
         model="gpt-3.5-turbo",
         messages=[
             {"role": "user", "content": prompts[idioma_destino]}
         ],
         temperature=0.3
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR de traducción]: {e}"


def guardar_en_archivo(timestamp, texto_da, texto_es, texto_en):
    nombre_archivo = f"transcripcion_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(nombre_archivo, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n")
        f.write(f"DANÉS:\n{texto_da}\n")
        f.write(f"ESPAÑOL:\n{texto_es}\n")
        f.write(f"INGLÉS:\n{texto_en}\n")
        f.write("=" * 60 + "\n")


def main():
    console.clear()
    console.rule("[bold green]🎧 Transcripción en vivo sincronizada por bloques")

    hilo_grabar = threading.Thread(target=grabar_y_transcribir, daemon=True)
    hilo_reproducir = threading.Thread(target=reproducir_y_mostrar, daemon=True)

    hilo_grabar.start()
    hilo_reproducir.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[red]⛔ Transcripción finalizada por el usuario.[/red]")


if __name__ == "__main__":
    main()
