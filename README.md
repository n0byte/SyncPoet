Hi für die Developer die gerne das Programm weiter Entickeln wollen, Bugs fixen oder einfach sich den source Code anschauen wollen oder wie es Funktioneirt.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Was braucht man um das Programm zu Entwickeln zu können?

🧰 Voraussetzungen
Um die Entwicklungsumgebung korrekt aufzusetzen, brauchst du Folgendes:

1. Python (Version < 3.12)
    - Das Projekt ist aktuell nicht kompatibel mit Python 3.12 oder höher.

2. Tauri
    - Wird für das Desktop-Frontend verwendet.

3. Rust
    - Wird von Tauri benötigt (z. B. für das native Packaging).

4. Eine Entwicklungsumgebung, z. B. Visual Studio Code mit folgenden Erweiterungen:
    - Python-Extension
    - Rust-Extension (z. B. rust-analyzer)

5. Node.js
    - Wird benötigt, um mit npm die JavaScript/Frontend-Abhängigkeiten zu verwalten.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Entwicklungsumgebung einrichten
1. Tauri installieren
Tauri benötigt einige systemweite Abhängigkeiten, je nach Betriebssystem. Die offizielle Anleitung ist hier sehr hilfreich:
👉 Tauri Setup Guide

Kurzfassung:

Node.js & npm installieren (empfohlen über nvm oder Node.js Downloads)

Rust installieren:

```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh```

Dann in deinem Projektverzeichnis:

```npm install```
```npm run tauri dev```

2. Python-Umgebung einrichten
3. Das hier ist nur Optional, weil man es auch Global machen kann.
   
Ein virtuelles Environment (venv) anlegen:

```python -m venv venv```
```venv\Scripts\activate```
Abhängigkeiten installieren:

pip install -r requirements.txt (requirements sind nur als veranschaulichung eigentlich kann man auch alles mit pip isntall packetname isntallieren)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

💡 Tipps

Nutze npm run tauri dev, um das Frontend mit Python-Backend im Entwicklungsmodus zu starten.

Backend und Frontend kommunizieren über einen lokalen HTTP-Server oder über Tauri Commands – je nach Setup.

Achte auf die Python-Version – neuere Versionen können zu Kompatibilitätsproblemen führen!

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Kurzer Überblick zur Projektstruktur:

Es gibt einen backend, src und src-tauri Ordner. 
    - In backend sind alle PYthon Dateien und Skripte für die Logic drinnen. 
    - Im src Verzeichnis (frontend) sind alle HTML, CSS, JS und asset Dateien.
    - Im src-tauri Verzeichnis sind Wichtige Rust und json Dateien in src-tauri gibt es nochmal einen src Ordner. darin ist eine main.rs und eine lib.rs. In den beiden Dateien wird konfiguriert #
      welche Skripte mit gestartet werden sollen beim start und welche ordner Init. werden und noch mehr.
    - Und dann gibt es noch einen icon Ordner da sind alle icons drinnen.

-
    [WICHTIG!] Die Dateistruktur "hier" passt nicht zu der in Tauri, hier sind nur alle Development Sachen und Dateien die von mir Stammen. Für mehr Informationen wie man die Dateien Ordnugsgemäß in das
               Tauri projekt einbindet kann, bitte schaut euch das Bild was direkt im Ordner liegt an.
    
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Informationen zu Tauri:

Kurz gesagt Tauri ist wie electron, ein Framework das Erlaubt Web Technologies wie HTMl, CSS und JS zu nutzen ium UI oder GUI zu Entwickeln und um Simple Apps, Programm eund Softwaren zu Entwickeln. Tauri ist deswegen eine gute Entscheidung, weil es 2 - 3x so
schnell wie Electron ist, weil es RUST als backend nutzt. Rust kann komplex sein, aber meistens wenn man mit Tauri arbeitet nutzt man es recht wenig. Eigentlich  nur für den Start von Dateien oder SImplen verbindungen (so habe ich bisher die Erfahrung gemacht gehabt).

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
