# Assistant Vocal Local

Ce projet est un assistant vocal simple qui fonctionne entièrement en local, sans nécessiter de connexion Internet. Il utilise la reconnaissance vocale pour transcrire ce que vous dites, puis utilise la synthèse vocale pour vous répondre.

## Fonctionnalités

-   **Reconnaissance Vocale (STT):** Utilise le modèle [Vosk](https://alphacephei.com/vosk/) pour une transcription vocale en français.
-   **Synthèse Vocale (TTS):** Utilise `pyttsx3` pour générer des réponses vocales.
-   **Fonctionnement Offline:** Toutes les opérations sont effectuées localement.
-   **Détection de Silence:** Arrête automatiquement l'écoute après une période de silence.

## Prérequis

-   Python 3.x
-   Un microphone branché et fonctionnel

## Installation

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_PROJET.git
    cd VOTRE_PROJET
    ```

2.  **Installez les dépendances :**
    Le script `start.bat` (pour Windows) installe automatiquement les dépendances listées dans `requirements.txt`. Vous pouvez également les installer manuellement :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

1.  **Exécutez le script `start.bat` (pour Windows) :**
    Double-cliquez sur le fichier `start.bat`. La première fois, il installera les dépendances, puis il lancera l'assistant vocal.

2.  **Exécutez le script Python directement :**
    ```bash
    python vocal_assistant.py
    ```

3.  **Parlez :**
    Une fois que le message "Microphone prêt et à l'écoute." s'affiche, vous pouvez commencer à parler.

4.  **Arrêter l'assistant :**
    Dites "au revoir" ou "arrête" pour quitter l'application. Vous pouvez également utiliser `Ctrl+C` dans la console.

## Fichiers du Projet

-   `vocal_assistant.py`: Le script principal de l'assistant vocal.
-   `requirements.txt`: La liste des dépendances Python.
-   `start.bat`: Un script batch pour faciliter le lancement sous Windows.
-   `README.md`: Ce fichier.
