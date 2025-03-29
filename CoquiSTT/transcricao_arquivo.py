import stt
import wave
import numpy as np
import os
import soundfile as sf
from pathlib import Path

def load_audio(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.wav':
        with wave.open(file_path, 'rb') as wf:
            rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
    elif file_extension in ['.mp3', '.flac', '.ogg']:
        audio_data, rate = sf.read(file_path)
        if len(audio_data.shape) > 1:  # Se for estéreo, converte para mono
            audio_data = audio_data.mean(axis=1)
        audio_data = (audio_data * 32767).astype(np.int16)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {file_extension}")
    
    return audio_data, rate

def transcreve_audio(arquivo_audio, modelo_path="model.tflite"):
    try:
        model = stt.Model(modelo_path)
        audio_data, sample_rate = load_audio(arquivo_audio)
        
        print(f"Transcrevendo arquivo: {arquivo_audio}")
        text = model.stt(audio_data)
        print("Transcrição:", text)
        return text
    except Exception as e:
        print(f"Erro durante a transcrição: {e}")
        return None

if __name__ == "__main__":
    arquivo_audio = "audio.wav"
    transcreve_audio(arquivo_audio)
