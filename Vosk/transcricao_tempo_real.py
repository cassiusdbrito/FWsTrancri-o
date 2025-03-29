import pyaudio
import wave
import json
import os
from vosk import Model, KaldiRecognizer
import sys
import time

class TranscricaoTempoReal:
    def __init__(self, modelo_path="modelo-vosk"):
        if not os.path.exists(modelo_path):
            print(f"Modelo não encontrado em {modelo_path}")
            print("Por favor, baixe um modelo em https://alphacephei.com/vosk/models")
            sys.exit(1)
            
        self.model = Model(modelo_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        
        # Configurações de áudio
        self.RATE = 16000
        self.CHUNK = 8000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        
    def inicializa_audio(self):
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=self.FORMAT,
                          channels=self.CHANNELS,
                          rate=self.RATE,
                          input=True,
                          frames_per_buffer=self.CHUNK)
            return p, stream
        except Exception as e:
            print(f"Erro ao inicializar áudio: {e}")
            sys.exit(1)
            
    def transcreve(self):
        p, stream = self.inicializa_audio()
        
        print("🎤 Iniciando gravação... (Pressione Ctrl+C para parar)")
        print("=" * 50)
        
        try:
            while True:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                if self.rec.AcceptWaveform(data):
                    resultado = json.loads(self.rec.Result())
                    if resultado["text"].strip():
                        print(f"[{time.strftime('%H:%M:%S')}] {resultado['text']}")
                        
        except KeyboardInterrupt:
            print("\nFinalizando gravação...")
        except Exception as e:
            print(f"Erro durante a execução: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            
def main():
    transcricao = TranscricaoTempoReal()
    transcricao.transcreve()

if __name__ == "__main__":
    main() 