from pocketsphinx import LiveSpeech
import os
from pydub import AudioSegment

def transcrever_audio(arquivo_audio):
    try:
        # Converter para WAV 16kHz mono se necessário
        if not arquivo_audio.endswith('.wav'):
            audio = AudioSegment.from_file(arquivo_audio)
            audio = audio.set_frame_rate(16000).set_channels(1)
            arquivo_wav = arquivo_audio.rsplit('.', 1)[0] + '.wav'
            audio.export(arquivo_wav, format='wav')
            arquivo_audio = arquivo_wav

        # Configurar o reconhecimento
        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm='modelo_pt_br',  # Pasta com o modelo em português
            lm='modelo_pt_br/portugues.lm',
            dic='modelo_pt_br/portugues.dic',
            audio_file=arquivo_audio
        )

        # Realizar a transcrição
        transcricao = []
        for phrase in speech:
            transcricao.append(str(phrase))

        # Salvar resultado
        nome_arquivo = os.path.splitext(arquivo_audio)[0]
        with open(f"{nome_arquivo}_transcricao.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(transcricao))

        print(f"✅ Transcrição concluída. Verifique '{nome_arquivo}_transcricao.txt'")
        return "\n".join(transcricao)

    except Exception as e:
        print(f"❌ Erro na transcrição: {e}")
        return None

if __name__ == "__main__":
    # Exemplo de uso
    arquivo_audio = "Áudios/Áudio do WhatsApp de 2025-04-02 à(s) 09.26.36_b6b5678e (online-audio-converter.com).wav"
    transcricao = transcrever_audio(arquivo_audio)
    if transcricao:
        print("\nTranscrição:", transcricao)