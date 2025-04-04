import os
import json
import logging
from datetime import datetime
import wave
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

class TranscricaoSimples:
    def __init__(self):
        """Inicializa o transcritor"""
        self.configurar_logging()
        self.model = Model("modelo/modelo-vosk")
        self.logger.info("Modelo Vosk carregado com sucesso")

    def configurar_logging(self):
        """Configura o sistema de logging"""
        self.logger = logging.getLogger("TranscricaoSimples")
        self.logger.setLevel(logging.INFO)
        
        # Criar diretório de logs
        os.makedirs("logs", exist_ok=True)
        
        # Configurar arquivo de log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        handler = logging.FileHandler(f"logs/transcricao_{timestamp}.log")
        handler.setLevel(logging.INFO)
        
        # Formato do log
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        
        # Adicionar handler ao logger
        self.logger.addHandler(handler)

    def transcrever_arquivo(self, arquivo_entrada, arquivo_saida=None):
        """Transcreve um arquivo de áudio"""
        try:
            self.logger.info(f"Iniciando transcrição: {arquivo_entrada}")
            
            # Verificar arquivo
            if not os.path.exists(arquivo_entrada):
                raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_entrada}")
            
            # Carregar e converter áudio
            audio = AudioSegment.from_file(arquivo_entrada)
            audio = audio.set_frame_rate(16000)  # Taxa de amostragem
            audio = audio.set_channels(1)        # Mono
            audio = audio.set_sample_width(2)    # 16 bits
            
            # Criar arquivo WAV temporário
            arquivo_temp = "temp.wav"
            audio.export(arquivo_temp, format="wav")
            
            # Abrir arquivo WAV
            wf = wave.open(arquivo_temp, "rb")
            
            # Criar reconhecedor
            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetWords(True)
            
            # Processar áudio
            resultados = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    resultado = json.loads(rec.Result())
                    if resultado.get("text"):
                        resultados.append(resultado["text"])
            
            # Processar último resultado
            resultado_final = json.loads(rec.FinalResult())
            if resultado_final.get("text"):
                resultados.append(resultado_final["text"])
            
            # Fechar arquivo
            wf.close()
            
            # Remover arquivo temporário
            os.remove(arquivo_temp)
            
            # Combinar resultados
            texto_completo = " ".join(resultados)
            
            # Salvar ou retornar resultado
            if arquivo_saida:
                with open(arquivo_saida, "w", encoding="utf-8") as f:
                    f.write(texto_completo)
                self.logger.info(f"Transcrição salva em: {arquivo_saida}")
            else:
                print(texto_completo)
            
            return texto_completo
            
        except Exception as e:
            self.logger.error(f"Erro na transcrição: {e}")
            raise

    def transcrever_pasta(self, pasta_entrada, pasta_saida=None):
        """Transcreve todos os arquivos de áudio em uma pasta"""
        try:
            self.logger.info(f"Processando pasta: {pasta_entrada}")
            
            # Criar pasta de saída se especificada
            if pasta_saida:
                os.makedirs(pasta_saida, exist_ok=True)
            
            # Listar arquivos de áudio
            extensoes = ('.wav', '.mp3', '.m4a', '.ogg', '.flac')
            arquivos = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(extensoes)]
            
            # Processar cada arquivo
            for arquivo in arquivos:
                entrada = os.path.join(pasta_entrada, arquivo)
                saida = None
                
                if pasta_saida:
                    nome_base = os.path.splitext(arquivo)[0]
                    saida = os.path.join(pasta_saida, f"{nome_base}.txt")
                
                try:
                    self.transcrever_arquivo(entrada, saida)
                except Exception as e:
                    self.logger.error(f"Erro ao processar {arquivo}: {e}")
            
            self.logger.info("Processamento da pasta concluído")
            
        except Exception as e:
            self.logger.error(f"Erro ao processar pasta: {e}")
            raise

def main():
    """Função principal para teste"""
    try:
        # Criar transcritor
        transcricao = TranscricaoSimples()
        
        # Exemplo de uso com um arquivo
        arquivo = "Áudios/Áudio do WhatsApp de 2025-04-02 à(s) 09.26.36_b6b5678e (online-audio-converter.com).wav"
        transcricao.transcrever_arquivo(arquivo, "saida.txt")
        
        # Exemplo de uso com uma pasta
        transcricao.transcrever_pasta("Áudios", "Transcrições")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main() 