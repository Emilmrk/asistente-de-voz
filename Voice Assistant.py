import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pyautogui
import difflib
import re
import time
import subprocess

# Inicializar el reconocedor y el motor de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Hablar texto
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Reconocer comandos de voz
def recognize_command():
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="es-ES").lower()
            print("Dijiste: " + command)
        except sr.UnknownValueError:
            speak("Lo siento, no pude entender lo que dijiste. Intenta de nuevo.")
            return ""
        except sr.RequestError as e:
            speak(f"No pude acceder al servicio de Google. Error: {e}. Verifica tu conexión.")
            return ""
        return command

# Coincidencia difusa
def fuzzy_match(command, keywords):
    command_cleaned = re.sub(r'[^\w\s]', '', command.lower())  # Limpiar entrada
    matches = difflib.get_close_matches(command_cleaned, keywords, cutoff=0.6)
    return matches[0] if matches else None

# Funciones para acciones
def handle_time():
    current_time = datetime.datetime.now().strftime("%H:%M %p")
    speak(f"La hora actual es {current_time}")

def handle_browser():
    speak("¿Qué te gustaría buscar?")
    query = recognize_command()
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")

def handle_typing():
    speak("¿Qué deseas escribir?")
    text = recognize_command()
    if text:
        pyautogui.write(text)
        speak(f"He escrito: {text}")

def open_application(app_name):
    app_paths = {
        "steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
        "calculadora": "calc.exe",
        "bloc de notas": "notepad.exe"
    }
    app_path = app_paths.get(app_name.lower())
    if app_path:
        try:
            subprocess.Popen(app_path)
            speak(f"Abriendo {app_name}...")
        except Exception as e:
            speak(f"No pude abrir {app_name}. Error: {e}")
    else:
        speak(f"No tengo configurada la aplicación {app_name}. Puedes agregarla en la lista.")

# Principal
def main():
    keywords = ["mi nombre", "hora", "abrir navegador", "escribir", "salir", "abrir"]
    app_keywords = ["steam", "calculadora", "bloc de notas"]  # Lista de aplicaciones soportadas
    speak("¡Hola! ¿En qué puedo ayudarte?")
    
    while True:
        command = recognize_command()
        matched = fuzzy_match(command, keywords)
        
        if matched == "mi nombre":
            speak("Me llamo Sofía, tu asistente personal.")
        elif matched == "hora":
            handle_time()
        elif matched == "abrir navegador":
            handle_browser()
        elif matched == "escribir":
            handle_typing()
        elif matched == "salir":
            speak("¡Adiós! ¡Que tengas un gran día!")
            break
        elif matched and matched.startswith("abrir"):  # Validar que `matched` no sea None
            # Extraer el nombre de la aplicación
            for app in app_keywords:
                if app in command:
                    open_application(app)  # Abrir la aplicación
                    break
            else:
                speak("No sé cómo abrir eso. Intenta con algo como Steam o Calculadora.")
        else:
            speak("No estoy segura de cómo responder a eso.")

        time.sleep(1)  # Pausa de 1 segundo entre iteraciones


if __name__ == "__main__":
    main()
