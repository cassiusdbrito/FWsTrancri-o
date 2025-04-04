import os
import ffmpeg
from pathlib import Path
import torch
import whisper
from pydub import AudioSegment
import site
import subprocess

# Configuração correta do FFmpeg
ffmpeg_dir = 'C:\\ffmpeg\\bin'  
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
os.environ["FFMPEG_BINARY"] = os.path.join(ffmpeg_dir, 'ffmpeg.exe')

# Verificação
try:
    subprocess.run([os.environ["FFMPEG_BINARY"], "-version"], check=True)
    print("FFmpeg configurado corretamente")
except Exception as e:
    print(f"Erro ao acessar FFmpeg: {e}")
    raise

model_path = "C:\\Users\\cassi\\fwsTransc\\Whisper\\tiny.pt"
model = whisper.load_model(model_path)

def listar_arquivos(pasta):
    return [os.path.join(pasta, f) for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]

def transforma_audios_pasta(pasta_path_inputs):
  lista_path_transform = []
  path= '/content'
  paths = listar_arquivos(pasta_path_inputs)
  pasta_transformada = os.path.join(path, "audios transformados")
  if not os.path.exists(pasta_transformada):
    os.makedirs(pasta_transformada)
  for input_audio in paths:
    if input_audio.endswith('.m4a'):
      output_audio = os.path.join(pasta_transformada, os.path.basename(input_audio).replace('.m4a', '.wav'))
    elif input_audio.endswith('.ogg'):
      output_audio = os.path.join(pasta_transformada, os.path.basename(input_audio).replace('.ogg', '.wav'))
    else:
      continue
    try:
        ffmpeg.input(input_audio).output(output_audio).run()
        lista_path_transform.append(output_audio)  # Adiciona o caminho transformado à lista
    except ffmpeg.Error as e:
        print(f"Erro ao converter {input_audio}: {e}")
  return lista_path_transform

def transforma_audio(input_audio, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(input_audio), "audios_transformados")
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Se for WAV, retorna o arquivo original
    if input_audio.endswith('.wav'):
        return input_audio
        
    if input_audio.endswith('.m4a'):
        output_audio = os.path.join(output_dir, os.path.basename(input_audio).replace('.m4a', '.wav'))
    elif input_audio.endswith('.ogg'):
        output_audio = os.path.join(output_dir, os.path.basename(input_audio).replace('.ogg', '.wav'))
    else:
        raise ValueError("Formato de áudio não suportado. Use '.m4a', '.ogg' ou '.wav'.")
    
    try:
        # Carrega o arquivo de áudio e exporta como WAV
        audio = AudioSegment.from_file(input_audio)
        audio.export(output_audio, format='wav')
        print("Arquivo salvo em:", output_audio)
        return output_audio
    except Exception as e:
        raise Exception(f"Erro ao converter áudio: {e}")


def whisper_transcrição(audio_path):
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {audio_path}")
            
        # Força o uso do FFmpeg configurado
        transcrição = model.transcribe(
            audio_path,
            fp16=False,  # Importante para CPU
            verbose=True  # Mostra logs do processo
        )
        return transcrição
    except Exception as e:
        print(f"Erro durante a transcrição: {str(e)}")
        raise


def formatar_transcricao(transcricao_completa):
    """Formata a transcrição para saída mais limpa"""
    texto = transcricao_completa['text']
    
    # Limpeza básica do texto
    texto = texto.strip()
    
    # Adiciona quebras de linha a cada período
    texto = texto.replace('. ', '.\n\n')
    
    # Remove espaços extras
    texto = ' '.join(texto.split())
    
    return texto

def main():
    # Verifica FFmpeg
    try:
        subprocess.run([os.environ["FFMPEG_BINARY"], "-version"], 
                      capture_output=True, check=True)
    except:
        print("ERRO: FFmpeg não está acessível")
        return

    # Verifica arquivo de áudio
    audio_file = os.path.join("Áudios", "audio_zap.wav")
    if not os.path.exists(audio_file):
        print(f"ERRO: Arquivo não encontrado - {os.path.abspath(audio_file)}")
        return

    try:
        print("🔊 Processando áudio...")
        audio_convertido = transforma_audio(audio_file)
        
        print("🎤 Transcrevendo áudio...")
        transcricao_completa = model.transcribe(
            audio_convertido,
            fp16=False,
            language='pt',
            verbose=False  # Remove logs do processo
        )
        
        # Formatação bonita da saída
        print("\n--- TRANSCRIÇÃO ---\n")
        print(formatar_transcricao(transcricao_completa))
        print("\n------------------")
        
        # Opcional: Salvar em arquivo
        with open("transcricao.txt", "w", encoding="utf-8") as f:
            f.write(transcricao_completa['text'])
        print("\nTranscrição salva em 'transcricao.txt'")
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")

if __name__ == "__main__":
    main()