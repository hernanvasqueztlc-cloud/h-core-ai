#!/usr/bin/env python3
"""
H-Core AI - Núcleo Personal de Asistencia Técnica y Ciberseguridad
Autor: Hernán Vásquez Ocaña
GitHub: https://github.com/hernanvasqueztlc-cloud/h-core-ai
"""

import requests
import os

MODELO = "phi3"
URL_API = "http://localhost:11434/api/chat"

BANNER = """
================================================================
  ██╗  ██╗       ██████╗ ██████╗ ██████╗ ███████╗
  ██║  ██║      ██╔════╝██╔═══██╗██╔══██╗██╔════╝
  ███████║█████╗██║     ██║   ██║██████╔╝█████╗  
  ██╔══██║╚════╝██║     ██║   ██║██╔══██╗██╔══╝  
  ██║  ██║      ╚██████╗╚██████╔╝██║  ██║███████╗
  ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
  Desarrollado por: Hernán Vásquez Ocaña | Kali Linux Edition
  Comandos: 'limpiar' (reinicia memoria) | 'salir' (terminar)
================================================================
"""

SYSTEM_PROMPT = (
    "Eres H-Core, el asistente técnico personal creado por Hernán Vásquez Ocaña. "
    "Te diriges a él como Hernán. Estás especializado en ciberseguridad, pentesting, "
    "redes, scripting (Python/Bash) y administración de sistemas Linux. "
    "Respondes sin rodeos, con precisión técnica y comandos listos para usar."
)

def iniciar_hcore():
    os.system("clear")
    print(BANNER)
    historial = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            entrada = input("\nHernán [H-Core] > ").strip()
            if not entrada:
                continue
            if entrada.lower() in ["salir", "exit", "quit"]:
                print("\n[H-Core] Sesión finalizada. Hasta luego, Hernán.")
                break
            if entrada.lower() == "limpiar":
                historial = [{"role": "system", "content": SYSTEM_PROMPT}]
                print("[H-Core] Memoria de conversación reiniciada.")
                continue

            historial.append({"role": "user", "content": entrada})
            print("Procesando...", end="\r")

            payload = {"model": MODELO, "messages": historial, "stream": False}
            response = requests.post(URL_API, json=payload, timeout=180)
            response.raise_for_status()

            respuesta_ia = response.json().get("message", {}).get("content", "")
            historial.append({"role": "assistant", "content": respuesta_ia})

            print(" " * 20, end="\r")
            print(f"\nH-Core > {respuesta_ia}")

        except requests.exceptions.ConnectionError:
            print("\n[Error] No se pudo conectar con Ollama. Ejecuta 'ollama serve'.")
            historial.pop()
        except KeyboardInterrupt:
            print("\n\n[H-Core] Interrupción detectada. Cerrando núcleo.")
            break
        except Exception as e:
            print(f"\n[Error inesperado] {e}")
            historial.pop()

if __name__ == "__main__":
    iniciar_hcore()
