import os
import json
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datasets import load_dataset
import logging
from datetime import datetime
import numpy as np

class FineTuningVosk:
    def __init__(self, modelo_base="facebook/wav2vec2-base", 
                 dataset_path="dataset/",
                 output_dir="modelo-finetuned"):
        self.modelo_base = modelo_base
        self.dataset_path = dataset_path
        self.output_dir = output_dir
        
        # Configurar logging
        self.configurar_logging()
        
        # Criar diretórios necessários
        os.makedirs(output_dir, exist_ok=True)
        
        # Inicializar modelo e processador
        self.processor = Wav2Vec2Processor.from_pretrained(modelo_base)
        self.model = Wav2Vec2ForCTC.from_pretrained(modelo_base)
        
    def configurar_logging(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"finetuning_{timestamp}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def preparar_dataset(self):
        """Prepara o dataset para fine-tuning"""
        try:
            dataset = load_dataset("json", data_files={
                "train": os.path.join(self.dataset_path, "train.json"),
                "test": os.path.join(self.dataset_path, "test.json")
            })
            
            def preparar_exemplo(exemplo):
                audio, sample_rate = torchaudio.load(exemplo["audio_path"])
                if sample_rate != 16000:
                    resampler = torchaudio.transforms.Resample(sample_rate, 16000)
                    audio = resampler(audio)
                
                inputs = self.processor(audio.squeeze().numpy(), 
                                      sampling_rate=16000,
                                      return_tensors="pt",
                                      padding=True)
                
                with self.processor.as_target_processor():
                    labels = self.processor(exemplo["text"]).input_ids
                
                inputs["labels"] = labels
                return inputs
            
            dataset = dataset.map(preparar_exemplo, remove_columns=dataset["train"].column_names)
            return dataset
            
        except Exception as e:
            logging.error(f"Erro ao preparar dataset: {e}")
            raise
            
    def treinar(self, epochs=3, batch_size=8, learning_rate=2e-5):
        """Executa o fine-tuning do modelo"""
        try:
            dataset = self.preparar_dataset()
            
            # Configurar treinamento
            training_args = {
                "output_dir": self.output_dir,
                "num_train_epochs": epochs,
                "per_device_train_batch_size": batch_size,
                "learning_rate": learning_rate,
                "save_total_limit": 2,
                "logging_steps": 100,
                "evaluation_strategy": "steps",
                "eval_steps": 500,
                "save_strategy": "steps",
                "save_steps": 500,
            }
            
            # Iniciar treinamento
            logging.info("Iniciando fine-tuning...")
            self.model.train()
            
            for epoch in range(epochs):
                logging.info(f"Epoch {epoch + 1}/{epochs}")
                
                for batch in dataset["train"].iter(batch_size=batch_size):
                    outputs = self.model(**batch)
                    loss = outputs.loss
                    loss.backward()
                    
                    # Atualizar pesos
                    optimizer = torch.optim.AdamW(self.model.parameters(), lr=learning_rate)
                    optimizer.step()
                    optimizer.zero_grad()
                    
                # Salvar checkpoint
                checkpoint_dir = os.path.join(self.output_dir, f"checkpoint-epoch-{epoch + 1}")
                self.model.save_pretrained(checkpoint_dir)
                self.processor.save_pretrained(checkpoint_dir)
                
            logging.info("Fine-tuning concluído!")
            
        except Exception as e:
            logging.error(f"Erro durante o fine-tuning: {e}")
            raise
            
    def avaliar(self):
        """Avalia o modelo após o fine-tuning"""
        try:
            dataset = self.preparar_dataset()
            self.model.eval()
            
            total_loss = 0
            num_exemplos = 0
            
            with torch.no_grad():
                for batch in dataset["test"].iter(batch_size=8):
                    outputs = self.model(**batch)
                    total_loss += outputs.loss.item()
                    num_exemplos += 1
            
            loss_medio = total_loss / num_exemplos
            logging.info(f"Loss médio na avaliação: {loss_medio}")
            return loss_medio
            
        except Exception as e:
            logging.error(f"Erro durante a avaliação: {e}")
            raise

def main():
    fine_tuning = FineTuningVosk()
    fine_tuning.treinar()
    fine_tuning.avaliar()

if __name__ == "__main__":
    main() 