# assemblyai_transcricao.py
import requests
import time
import os
from pydub import AudioSegment
import ffmpeg

API_KEY = "d0e7eb12338446b48f7e8d0d65d9c0f8"  
AUDIO_PATH = r"C:\Users\cassi\fwsTransc\Áudios\audio_zap.wav"

def converter_para_wav_se_necessario(arquivo_original):
    """Converte para WAV 16kHz mono se não estiver no formato correto"""
    try:
        audio = AudioSegment.from_file(arquivo_original)
        print(f"Duração: {len(audio)/1000}s | Canais: {audio.channels} | Taxa de amostragem: {audio.frame_rate}Hz")
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        nome_base = os.path.splitext(arquivo_original)[0]
        arquivo_wav = f"{nome_base}_converted.wav"
        audio.export(arquivo_wav, format="wav", parameters=["-ac", "1", "-ar", "16000"])
        print(f"Áudio convertido para WAV: {arquivo_wav}")
        return arquivo_wav
    except Exception as e:
        print(f"Erro na conversão: {e}")
        return None

def converter_com_ffmpeg(input_path):
    output_path = input_path.replace(".wav", "_fixed.wav")
    ffmpeg.input(input_path).output(
        output_path,
        acodec='pcm_s16le',
        ac=1,
        ar='16k'
    ).run(overwrite_output=True)
    return output_path

def transcrever_audio_ptbr(arquivo_audio):
    """Realiza transcrição com configurações otimizadas para português"""
    try:
        # 1. Converter áudio se necessário
        arquivo_processado = converter_para_wav_se_necessario(arquivo_audio)
        if not arquivo_processado:
            arquivo_processado = converter_com_ffmpeg(arquivo_audio)

        if not arquivo_processado: return None

        # 2. Upload do arquivo
        print("Fazendo upload do áudio para AssemblyAI...")
        headers = {"authorization": API_KEY}
        
        # Método de upload direto
        with open(arquivo_processado, "rb") as f:
            upload_response = requests.post(
                "https://api.assemblyai.com/v2/upload",
                headers=headers,
                data=f
            )
        
        if upload_response.status_code != 200:
            print(f"Erro no upload: {upload_response.json()}")
            return None
            
        audio_url = upload_response.json()["upload_url"]
        print(f"Upload concluído. URL: {audio_url}")

        # 3. Configuração para português brasileiro
        print("Iniciando transcrição...")
        transcript_response = requests.post(
            "https://api.assemblyai.com/v2/transcript",
            json={
                "audio_url": audio_url,
                "language_code": "pt",
                "punctuate": True,
                "format_text": True,
                "speaker_labels": True
            },
            headers={
                "authorization": API_KEY,
                "content-type": "application/json"
            }
        )
        
        # Verificação adicional da resposta
        if transcript_response.status_code != 200:
            print(f"Erro na solicitação de transcrição: {transcript_response.text}")
            return None
            
        transcript_data = transcript_response.json()
        if "id" not in transcript_data:
            print("Resposta inesperada da API:", transcript_data)
            return None
            
        transcript_id = transcript_data["id"]
        print(f"ID da transcrição: {transcript_id}")

        # 4. Monitoramento do progresso
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            status_response = requests.get(polling_endpoint, headers=headers)
            status = status_response.json()
            
            if status["status"] == "completed":
                print("\nTranscrição concluída com sucesso!")
                return status["text"]
                
            elif status["status"] == "error":
                print("\nErro na transcrição:", status.get("error", "Desconhecido"))
                return None
                
            print(".", end="", flush=True)
            time.sleep(5)

    except Exception as e:
        print(f"\nErro no processo: {str(e)}")
        return None

if __name__ == "__main__":
    print("=== Transcrição de Áudio em Português ===")
    transcricao = transcrever_audio_ptbr(AUDIO_PATH)
    
    if transcricao:
        print("\n=== Transcrição Final ===")
        print(transcricao)
    else:
        print("Falha na transcrição. Verifique os detalhes acima.")