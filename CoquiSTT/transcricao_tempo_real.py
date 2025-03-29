import pyaudio
import numpy as np
import stt
import sys
import time

RATE = 16000  # Taxa de amostragem
CHUNK = 1024  # Tamanho do buffer

def inicializa_audio():
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        return p, stream
    except Exception as e:
        print(f"Erro ao inicializar áudio: {e}")
        sys.exit(1)

def main():
    try:
        model = stt.Model("model.tflite")
        p, stream = inicializa_audio()
        
        print("Iniciando gravação... (Pressione Ctrl+C para parar)")
        print("=" * 50)
        
        while True:
            audio_buffer = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(audio_buffer, dtype=np.int16)
            text = model.stt(audio_data)
            if text.strip():
                print(f"[{time.strftime('%H:%M:%S')}] {text}")
                
    except KeyboardInterrupt:
        print("\nFinalizando gravação...")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
