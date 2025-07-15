import vosk
import pyaudio
# import pyttsx3 # La synthèse vocale est temporairement désactivée pour une meilleure compatibilité
import json
import os
import requests
import zipfile
import io

# --- Configuration ---
MODEL_NAME = "vosk-model-fr-0.22"
MODEL_PATH = "model"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"
INPUT_DEVICE_INDEX = None  # Laisser à None pour utiliser le microphone par défaut
SAMPLE_RATE = 16000
CHUNK_SIZE = 8000
SILENCE_THRESHOLD = 2.0  # Durée du silence en secondes pour arrêter l'enregistrement

def list_audio_devices(p):
    """Liste tous les périphériques d'entrée audio disponibles."""
    print("Liste des périphériques audio d'entrée :")
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"  - Périphérique {i}: {device_info.get('name')}")

def get_default_input_device_info(p):
    """Retourne les informations du périphérique d'entrée par défaut."""
    try:
        return p.get_default_input_device_info()
    except IOError as e:
        print(f"Avertissement : Impossible de trouver le périphérique d'entrée par défaut. Erreur : {e}")
        return None

def download_and_unzip_model():
    """Télécharge et décompresse le modèle Vosk si non présent."""
    if os.path.exists(MODEL_PATH):
        print(f"Le dossier du modèle '{MODEL_PATH}' existe déjà.")
        return
    
    print(f"Téléchargement du modèle '{MODEL_NAME}' depuis {MODEL_URL}...")
    try:
        r = requests.get(MODEL_URL, allow_redirects=True, stream=True)
        r.raise_for_status()
        
        print("Décompression du modèle...")
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall(".")
        
        os.rename(MODEL_NAME, MODEL_PATH)
        print(f"Modèle '{MODEL_NAME}' téléchargé et placé dans le dossier '{MODEL_PATH}'.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de téléchargement : {e}")
        exit()
    except zipfile.BadZipFile:
        print("Erreur : Le fichier téléchargé n'est pas un fichier zip valide.")
        exit()
    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de la configuration du modèle : {e}")
        exit()

# --- Initialisation ---
download_and_unzip_model()

# --- Initialisation STT (Speech-to-Text) ---
if not os.path.exists(MODEL_PATH):
    print(f"Erreur : Le dossier du modèle '{MODEL_PATH}' est introuvable.")
    exit()

try:
    model = vosk.Model(MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    print("Modèle de reconnaissance vocale chargé.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle Vosk : {e}")
    exit()

# --- Initialisation de l'entrée Audio ---
p = None
stream = None
try:
    p = pyaudio.PyAudio()
    list_audio_devices(p)

    default_device_info = get_default_input_device_info(p)
    if default_device_info:
        default_index = default_device_info['index']
        default_name = default_device_info['name']
        prompt = f"Entrez l'index du périphérique (ou laissez vide pour utiliser le périphérique par défaut : {default_index} - {default_name}) : "
    else:
        prompt = "Entrez l'index du périphérique : "

    try:
        input_device_index_str = input(prompt)
        if input_device_index_str.strip():
            INPUT_DEVICE_INDEX = int(input_device_index_str)
        elif default_device_info:
            INPUT_DEVICE_INDEX = default_device_info['index']

    except ValueError:
        print("Entrée invalide. Utilisation du périphérique par défaut si disponible.")
        if default_device_info:
            INPUT_DEVICE_INDEX = default_device_info['index']
    except Exception as e:
        print(f"Une erreur est survenue lors de la sélection du périphérique : {e}")
        exit()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK_SIZE)
    stream.start_stream()
    print("Microphone prêt et à l'écoute.")
except Exception as e:
    print(f"Erreur critique : Impossible d'ouvrir le flux audio.")
    print(f"Vérifiez qu'un microphone est bien branché et autorisé. Erreur PyAudio : {e}")
    exit()

def speak(text):
    """Affiche la réponse de l'assistant."""
    print(f"Assistant > {text}")

def listen():
    """Capture l'audio du micro, détecte le silence et retourne le texte reconnu."""
    print("\nParlez maintenant...")
    silent_chunks = 0
    max_silent_chunks = int(SILENCE_THRESHOLD * SAMPLE_RATE / CHUNK_SIZE)
    
    while True:
        try:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get('text', '')
                if text:
                    return text.strip()
            else:
                partial_result = json.loads(recognizer.PartialResult())
                if not partial_result.get('partial', ''):
                    silent_chunks += 1
                    if silent_chunks > max_silent_chunks:
                        return None
                else:
                    silent_chunks = 0
        except IOError as e:
            print(f"Erreur de lecture du microphone : {e}. L'assistant va s'arrêter.")
            return "error"

def main():
    """Boucle principale de l'assistant vocal."""
    try:
        speak("Bonjour ! Je suis prêt à écouter.")
        while True:
            text = listen()
            
            if text == "error":
                break
                
            if text:
                print(f"Vous avez dit : {text}")
                
                if "au revoir" in text.lower() or "arrête" in text.lower():
                    speak("Au revoir !")
                    break
                
                response = f"J'ai bien entendu : \"{text}\""
                speak(response)
            else:
                print("Silence détecté, en attente de la prochaine commande.")

    except KeyboardInterrupt:
        print("\nArrêt manuel de l'assistant. À bientôt !")
    finally:
        if stream and stream.is_active():
            stream.stop_stream()
            stream.close()
        if p:
            p.terminate()
        print("Ressources audio libérées.")

if __name__ == "__main__":
    main()