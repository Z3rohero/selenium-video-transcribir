from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import speech_recognition as sr
import os
import sys

class BrowserAutoSearch:
    """Clase que automatiza la búsqueda en navegadores y la grabación de audio."""

    def __init__(self):
        """Inicializa la instancia de BrowserAutoSearch configurando el navegador."""
        self.browser = self._initialize_browser()

    def _initialize_browser(self):
        """Inicializa el navegador basado en los navegadores instalados (Firefox o Chrome)."""
        browsers = {
            "firefox": {
                "manager": GeckoDriverManager,
                "service": FirefoxService,
                "options": webdriver.FirefoxOptions(),
                "driver": webdriver.Firefox
            },
            "chrome": {
                "manager": ChromeDriverManager,
                "service": ChromeService,
                "options": webdriver.ChromeOptions(),
                "driver": webdriver.Chrome
            }
        }
        
        for browser_name, browser_info in browsers.items():
            try:
                return browser_info["driver"](
                    service=browser_info["service"](browser_info["manager"]().install()),
                    options=browser_info["options"]
                )
            except Exception as e:
                print(f"Error al iniciar {browser_name}: {e}")
        raise Exception("No se pudo iniciar ningún navegador. Asegúrate de tener Firefox o Chrome instalados.")

    def play_video(self, video_selector="VfPpkd-kBDsod"):
        """Busca y da play al video en la página web."""
        try:
            play_button = WebDriverWait(self.browser, 10).until(
               # EC.element_to_be_clickable((By.CSS_SELECTOR, ".VYBDae-Bz112c-kBDsod-Rtc0Jf .VfPpkd-kBDsod"))
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VYBDae-Bz112c-kBDsod-Rtc0Jf')]//svg[@viewBox='0 -960 960 960']"))
            )
            play_button.click()
            print("El video ha comenzado a reproducirse.")
        except Exception as e:
            print(f"Error al intentar dar play al video: {e}")

    def accept_cookies(self, button_selector="L2AGLb"):
        """Acepta el anuncio de cookies en una página web."""
        try:
            accept_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, button_selector))
            )
            print("Botón de cookies encontrado:", accept_button)  # Imprime el botón
            accept_button.click()
        except Exception as e:
            print(f"Error al aceptar cookies: {e}")

    def iniciar_grabacion_audio(self, nombre_archivo="audio_output.wav"):
        """Inicia la grabación de audio con ffmpeg desde el sistema."""
        if os.name == "posix":
             input_format = "avfoundation" if sys.platform == "darwin" else "pulse"
            # Verifica si es macOS o Linux
        elif os.name == "nt":
            input_format = "dshow"
            # Windows
        else:
            raise Exception("Sistema operativo no compatible para la grabación de audio.")

        print(f"este es el formato para captura{input_format}") 
        comando_ffmpeg = [
            "ffmpeg",
            "-f", input_format,
            "-i", ":0",
            nombre_archivo
        ]

        return subprocess.Popen(comando_ffmpeg)


    def detener_grabacion_audio(self, proceso_ffmpeg):
        """Detiene la grabación de audio de ffmpeg."""
        proceso_ffmpeg.terminate()

    def audio_a_texto(self, ruta_audio):
        """Convierte audio WAV a texto usando Whisper."""
        # Cargar el modelo de Whisper
        modelo = whisper.load_model("base")  # Puedes usar otros modelos como 'small', 'medium', etc.
        
        # Realizar la transcripción
        resultado = modelo.transcribe(ruta_audio)
        
        # Obtener el texto transcrito
        texto = resultado['text']
        return texto
    def quit(self):
        """Cierra el navegador y finaliza la instancia del WebDriver."""
        self.browser.quit()


def main():
    # Crear instancia de BrowserAutoSearch
    navegador = BrowserAutoSearch()

    # Abre la URL del video y realiza acciones
    #url = input("Introduce el enlace del video: ")
    url="https://drive.google.com/file/d/1a9MT8N8qpYMcWNJ0RznSRmlx3QqD7pdA/view"
    navegador.browser.get(url)
    time.sleep(3)  # Espera unos segundos para cargar la página completamente

     # Imprime el botón de aceptar cookies (si está presente)
    # navegador.accept_cookies()

    print(f"===============Iniciado el play ======")

    # Inicia la reproducción del video
    navegador.play_video()

    # Iniciar grabación de audio
    print("Iniciando grabación de audio...")
    proceso_ffmpeg = navegador.iniciar_grabacion_audio()

    # Define la duración de la grabación
    duracion = 60  # Ajusta según la duración del video
    time.sleep(duracion)

    # Detener la grabación de audio
    navegador.detener_grabacion_audio(proceso_ffmpeg)

    # Convierte el audio grabado a texto
    print("Transcribiendo audio a texto...")
    texto = navegador.audio_a_texto("audio_output.wav")
    print("Texto transcrito:", texto)

    # Guarda la transcripción en un archivo
    with open("transcripcion.txt", "w", encoding="utf-8") as archivo:
        archivo.write(texto)
    print("Transcripción completada y guardada en 'transcripcion.txt'.")

    # Cierra el navegador
    navegador.quit()


# Asegúrate de que el código principal se ejecute correctamente
if __name__ == "__main__":
    main()
