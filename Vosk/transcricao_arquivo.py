import wave
import json
import os
from vosk import Model, KaldiRecognizer
import soundfile as sf
import numpy as np
from pathlib import Path

class TranscricaoArquivo:
    def __init__(self, modelo_path="modelo-vosk"):
        if not os.path.exists(modelo_path):
            print(f"Modelo não encontrado em {modelo_path}")
            print("Por favor, baixe um modelo em https://alphacephei.com/vosk/models")
            raise FileNotFoundError(f"Modelo não encontrado: {modelo_path}")
            
        self.model = Model(modelo_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        
    def carrega_audio(self, arquivo_path):
        if not os.path.exists(arquivo_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_path}")
        
        extensao = Path(arquivo_path).suffix.lower()
        
        if extensao == '.wav':
            with wave.open(arquivo_path, 'rb') as wf:
                if wf.getframerate() != 16000:
                    print("Aviso: Taxa de amostragem diferente de 16kHz")
                frames = wf.readframes(wf.getnframes())
                return frames
        elif extensao in ['.mp3', '.flac', '.ogg']:
            audio_data, sample_rate = sf.read(arquivo_path)
            if len(audio_data.shape) > 1:  # Se for estéreo, converte para mono
                audio_data = audio_data.mean(axis=1)
            if sample_rate != 16000:
                print("Aviso: Taxa de amostragem diferente de 16kHz")
            # Converte para o formato esperado pelo Vosk
            audio_data = (audio_data * 32767).astype(np.int16)
            return audio_data.tobytes()
        else:
            raise ValueError(f"Formato de arquivo não suportado: {extensao}")
    
    def transcreve(self, arquivo_path):
        try:
            print(f"Transcrevendo arquivo: {arquivo_path}")
            audio_data = self.carrega_audio(arquivo_path)
            
            if self.rec.AcceptWaveform(audio_data):
                resultado = json.loads(self.rec.Result())
                print("Transcrição:", resultado["text"])
                return resultado["text"]
            else:
                print("Não foi possível transcrever o áudio")
                return None
                
        except Exception as e:
            print(f"Erro durante a transcrição: {e}")
            return None

def main():
    transcricao = TranscricaoArquivo()
    arquivo_audio = "audio.wav"
    transcricao.transcreve(arquivo_audio)

if __name__ == "__main__":
    main() 