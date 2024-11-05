import subprocess
import webbrowser
import time
import os
import sys
from threading import Thread

def run_streamlit():
    """Ejecuta el servidor de Streamlit"""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

def open_browser():
    """Abre el navegador después de un pequeño retraso"""
    time.sleep(3)  # Espera 3 segundos para que el servidor inicie
    webbrowser.open('http://localhost:8501')

if __name__ == "__main__":
    # Asegurarse de que estamos en el directorio correcto
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    # Iniciar el servidor de Streamlit en un hilo separado
    server_thread = Thread(target=run_streamlit)
    server_thread.start()
    
    # Abrir el navegador
    open_browser()
    
    # Mantener el programa corriendo
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\nCerrando la aplicación...")
        sys.exit(0)
