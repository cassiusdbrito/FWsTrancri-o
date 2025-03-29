import coqui_stt_training
import os
import logging
from datetime import datetime
import json

def configurar_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"treinamento_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def validar_parametros(dataset_treino, dataset_teste, modelo_pretreinado):
    if not os.path.exists(dataset_treino):
        raise FileNotFoundError(f"Dataset de treino não encontrado: {dataset_treino}")
    if not os.path.exists(dataset_teste):
        raise FileNotFoundError(f"Dataset de teste não encontrado: {dataset_teste}")
    if not os.path.exists(modelo_pretreinado):
        raise FileNotFoundError(f"Modelo pré-treinado não encontrado: {modelo_pretreinado}")
    
    if epochs <= 0:
        raise ValueError("Número de epochs deve ser maior que 0")
    if learning_rate <= 0:
        raise ValueError("Learning rate deve ser maior que 0")
    if not 0 <= dropout_rate <= 1:
        raise ValueError("Dropout rate deve estar entre 0 e 1")

def TreinaModelo(dataset_treino, dataset_teste, modelo_pretreinado, epochs=50, learning_rate=0.0001, dropout_rate=0.15):
    configurar_logging()
    logging.info("Iniciando processo de treinamento")
    
    try:
        validar_parametros(dataset_treino, dataset_teste, modelo_pretreinado)
        
        # Criar diretório para checkpoints
        checkpoint_dir = "checkpoints"
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Preparar os parâmetros para treinamento
        parametros = {
            'train_files': dataset_treino,
            'test_files': dataset_teste,
            'epochs': epochs,
            'learning_rate': learning_rate,
            'dropout_rate': dropout_rate,
            'load_checkpoint': modelo_pretreinado,
            'checkpoint_dir': checkpoint_dir,
            'save_checkpoint_steps': 1000
        }
        
        # Salvar configuração
        config_file = os.path.join(checkpoint_dir, "config.json")
        with open(config_file, 'w') as f:
            json.dump(parametros, f, indent=4)
        
        # Iniciar o treinamento
        logging.info("Iniciando treinamento com os seguintes parâmetros:")
        for key, value in parametros.items():
            logging.info(f"{key}: {value}")
            
        coqui_stt_training.train(**parametros)
        logging.info("Treinamento concluído com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro durante o treinamento: {e}")
        raise

if __name__ == "__main__":
    # dataset_treino = "dataset/train.tsv"
    # dataset_teste = "dataset/test.tsv"
    # modelo_pretreinado = "modelo-pretreinado.tflite"
    
    # TreinaModelo(dataset_treino, dataset_teste, modelo_pretreinado)
    