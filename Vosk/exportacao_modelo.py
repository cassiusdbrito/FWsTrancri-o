import os
import json
import logging
from datetime import datetime
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class ExportacaoModelo:
    def __init__(self, modelo_path="modelo-finetuned", output_dir="modelo-final"):
        self.modelo_path = modelo_path
        self.output_dir = output_dir
        
        # Configurar logging
        self.configurar_logging()
        
        # Criar diretório de saída
        os.makedirs(output_dir, exist_ok=True)
        
    def configurar_logging(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"exportacao_{timestamp}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def exportar(self):
        """Exporta o modelo para o formato Vosk"""
        try:
            logging.info(f"Iniciando exportação do modelo de {self.modelo_path}")
            
            # Carregar modelo e processador
            model = Wav2Vec2ForCTC.from_pretrained(self.modelo_path)
            processor = Wav2Vec2Processor.from_pretrained(self.modelo_path)
            
            # Salvar modelo e processador
            model.save_pretrained(self.output_dir)
            processor.save_pretrained(self.output_dir)
            
            # Verificar arquivos exportados
            arquivos_esperados = [
                "config.json",
                "pytorch_model.bin",
                "special_tokens_map.json",
                "tokenizer_config.json",
                "vocab.json"
            ]
            
            for arquivo in arquivos_esperados:
                caminho = os.path.join(self.output_dir, arquivo)
                if not os.path.exists(caminho):
                    raise FileNotFoundError(f"Arquivo {arquivo} não foi exportado corretamente")
                logging.info(f"Arquivo {arquivo} exportado com sucesso")
            
            logging.info("Exportação concluída com sucesso!")
            return True
            
        except Exception as e:
            logging.error(f"Erro durante a exportação: {e}")
            return False

def main():
    exportacao = ExportacaoModelo()
    if exportacao.exportar():
        print("Exportação concluída com sucesso!")
    else:
        print("Falha na exportação do modelo.")

if __name__ == "__main__":
    main() 