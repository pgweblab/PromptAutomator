Prompt Automator

🔱 Interfaccia desktop moderna per automatizzare sequenze di prompt, click e digitazione in applicazioni AI o ambienti testuali.

✨ Caratteristiche principali

GUI moderna con stile scuro (Tkinter + ttk)

Registrazione di coordinate Start e Artifact con il mouse

Inserimento automatizzato di prompt in sequenza tramite pyautogui

Timer personalizzabile tra ogni step (default: 5 minuti)

Salvataggio/caricamento istruzioni in JSON con relative coordinate

Scroll dinamico e auto-resize dei campi istruzione

Sistema multithreaded per automazione asincrona e non bloccante

📆 Requisiti

Python 3.9 o superiore

Ambiente Windows consigliato

Moduli Python necessari:

pip install pyautogui pynput

🚀 Avvio rapido

Clona il repository:

git clone https://github.com/tuo-utente/ai-prompt-automator.git
cd ai-prompt-automator

Installa i requisiti:

pip install -r requirements.txt

Avvia l’applicazione:

python ai_prompt_automator.py

🧠 Utilizzo

Registra le coordinate del campo iniziale (Start) e di destinazione (Artifact)

Inserisci una o più istruzioni testuali

Imposta un timer (in secondi) tra un’inserzione e l’altra

Avvia l’automazione e lascia che lo script faccia il resto

📁 Salvataggio & Caricamento

I file .json contengono:

Lista delle istruzioni

Timer personalizzato

Coordinate registrate

🖼️ Screenshot

Inserisci qui un'immagine se vuoi mostrarla nel repo

📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per i dettagli.

