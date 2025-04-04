# nemo_transcricao.py
import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
import os

'''
    erro de instalaçãp ocorre porque o pacote requer o Microsoft Visual C++ Build Tools 
    para compilar extensões em C++
'''

def transcrever_audio(arquivo_audio):
    try:
        # 1. Converter áudio para formato compatível (16kHz mono)
        audio = AudioSegment.from_file(arquivo_audio)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio_convertido = "audio_convertido.wav"
        audio.export(audio_convertido, format="wav")

        # 2. Carregar modelo PT-BR
        modelo = nemo_asr.models.EncDecCTCModel.from_pretrained(
            "nvidia/stt_pt_quartznet15x5"
        )

        # 3. Transcrever
        transcricao = modelo.transcribe([audio_convertido])

        # 4. Salvar resultado
        nome_arquivo = os.path.splitext(arquivo_audio)[0]
        with open(f"{nome_arquivo}_transcricao.txt", "w", encoding="utf-8") as f:
            f.write(transcricao[0])

        # 5. Limpar arquivo temporário
        os.remove(audio_convertido)
        
        print(f"Transcrição concluída. Verifique '{nome_arquivo}_transcricao.txt'")
        return transcricao[0]
        
    except Exception as e:
        print(f"Erro na transcrição: {e}")
        return None

if __name__ == "__main__":
    # Exemplo de uso
    arquivo_audio = r'C:\Users\cassi\fwsTransc\Áudios\audio_zap.wav'
    transcricao = transcrever_audio(arquivo_audio)
    if transcricao:
        print("\nTranscrição:", transcricao)