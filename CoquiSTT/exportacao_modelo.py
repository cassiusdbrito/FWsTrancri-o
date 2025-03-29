import coqui_stt_training
import os
import logging
from datetime import datetime

def configurar_logging():
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

def ExportaModelo(modelo_treinado, pasta_export):
    configurar_logging()
    logging.info("Iniciando processo de exportação")
    
    try:
        # Verificar se o modelo treinado existe
        if not os.path.exists(modelo_treinado):
            raise FileNotFoundError(f"Diretório do modelo treinado não encontrado: {modelo_treinado}")
        
        # Criar diretório de exportação se não existir
        os.makedirs(pasta_export, exist_ok=True)
        
        logging.info(f"Exportando modelo de {modelo_treinado} para {pasta_export}")
        coqui_stt_training.export(checkpoint_dir=modelo_treinado, export_dir=pasta_export)
        
        # Verificar se os arquivos foram exportados
        arquivos_esperados = ['model.tflite', 'model.pbmm']
        for arquivo in arquivos_esperados:
            caminho = os.path.join(pasta_export, arquivo)
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo {arquivo} não foi exportado corretamente")
        
        logging.info("Modelo exportado com sucesso!")
        return True
        
    except Exception as e:
        logging.error(f"Erro durante a exportação: {e}")
        return False

if __name__ == "__main__":
    modelo_treinado = "modelo-treinado/"
    pasta_export = "modelo-final/"
    
    if ExportaModelo(modelo_treinado, pasta_export):
        print("Exportação concluída com sucesso!")
    else:
        print("Falha na exportação do modelo.")
