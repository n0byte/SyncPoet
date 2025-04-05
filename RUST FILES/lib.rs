use std::process::{Command, Stdio};
use std::fs;
use tauri::Manager;

#[cfg(windows)]
use std::os::windows::process::CommandExt;
#[cfg(windows)]
const DETACHED_PROCESS: u32 = 0x00000008;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hallo, {}!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let context = tauri::generate_context!();

    let app = tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .build(context)
        .expect("❌ Fehler beim Erstellen der App");

    let python_cmd = if cfg!(windows) { "python.exe" } else { "python3" };

    // Im Build-Modus liegt server.py im Ordner: resource_dir/_up_/backend/server.py
    let build_path = app
        .path()
        .resource_dir()
        .ok()
        .map(|res_dir| res_dir.join("_up_").join("backend").join("server.py"));

    // Pfad im Dev-Modus (relativ zur Projektstruktur)
    let dev_path = std::path::Path::new("../backend/server.py");

    // Versuche zuerst den Build-Pfad, ansonsten den Dev-Pfad
    let python_script = build_path.filter(|p| p.exists()).or_else(|| {
        if dev_path.exists() {
            Some(dev_path.to_path_buf())
        } else {
            None
        }
    });

    // Starte das Python-Skript oder logge einen Fehler
    if let Some(script_path) = python_script {
        println!("🚀 Starte Python-Skript: {:?}", script_path);
        #[cfg(windows)]
        {
            // Starte den Prozess detached, damit er unabhängig vom Hauptprozess läuft
            match Command::new(python_cmd)
                .arg(script_path)
                .creation_flags(DETACHED_PROCESS)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
            {
                Ok(_child) => {
                    println!("✅ Python-Prozess erfolgreich detached gestartet.");
                }
                Err(e) => {
                    println!("❌ Fehler beim Starten von Python: {:?}", e);
                }
            }
        }
        #[cfg(not(windows))]
        {
            match Command::new(python_cmd)
                .arg(script_path)
                .stdout(Stdio::inherit())
                .stderr(Stdio::inherit())
                .spawn()
            {
                Ok(mut child) => {
                    std::thread::spawn(move || {
                        if let Err(e) = child.wait() {
                            println!("❌ Python-Prozess ist abgestürzt: {:?}", e);
                        }
                    });
                }
                Err(e) => {
                    println!("❌ Fehler beim Starten von Python: {:?}", e);
                }
            }
        }
    } else {
        println!("⚠️ Kein server.py gefunden – weder im Build noch im Dev!");
    }    

    // Starte die Tauri App
    app.run(|_app_handle, _event| {});
}