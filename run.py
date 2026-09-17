"""
Entrypoint CLI / Launcher for MY EARS.
Permite ejecutar el pipeline directamente desde consola o levantar el servidor web.
"""

import argparse
import sys
from core.pipeline import MyEarsPipeline

def main():
    parser = argparse.ArgumentParser(description="MY EARS - Spotify Mood & Content Engine")
    parser.add_argument("--experience", "-e", type=str, help="Texto o vivencia del día a procesar")
    parser.add_argument("--volume", "-v", type=int, default=1, help="Número de volumen de la sesión")
    parser.add_argument("--server", "-s", action="store_true", help="Iniciar el dashboard web local")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Puerto para el servidor web")

    args = parser.parse_args()

    if args.server:
        import uvicorn
        print(f"🚀 Iniciando servidor MY EARS en http://127.0.0.1:{args.port} ...")
        uvicorn.run("web.app:app", host="127.0.0.1", port=args.port, reload=False)
        return

    pipeline = MyEarsPipeline()

    if args.experience:
        experience = args.experience
    else:
        print("\n=======================================================")
        print("          🎧 MY EARS : SPOTIFY MOOD ENGINE           ")
        print("=======================================================\n")
        experience = input("Cuéntame tu vivencia o cómo te sientes hoy: ").strip()
        if not experience:
            print("No se ingresó ninguna experiencia. Saliendo.")
            return

    print("\n⏳ Procesando vivencia, extrayendo esencia y curando lista...")
    result = pipeline.process_experience(experience, volume=args.volume)

    print("\n✅ PLAYLIST GENERADA EXITOSAMENTE:")
    print(f"📌 Título: {result['selected_title']}")
    print(f"🔗 Spotify Link: {result['playlist'].get('url')}")
    print(f"📝 Descripción: {result['description']}")
    print("\n🎶 CANCIONES SELECCIONADAS:")
    for idx, track in enumerate(result['tracks'], 1):
        print(f"   {idx}. {track['title']} - {track['artist']}")

    print("\n📣 GUIONES DE DIFUSIÓN GENERADOS:")
    for script in result['campaign']['scripts']:
        print(f"\n--- {script['creator']} ({script['format']}) ---")
        print(f"🔥 Hook (0-3s): {script['hook_0_to_3s']}")
        print(f"🎬 Dirección visual: {script['visual_direction']}")
        print(f"🎙️ Voiceover: {script['voiceover_body']}")
        print(f"🔗 CTA: {script['call_to_action']}")
    print("\n=======================================================\n")

if __name__ == "__main__":
    main()
