# FWsTrancri-o Vosk

Sistema de transcrição de áudio usando Vosk com suporte a fine-tuning.

## Funcionalidades

- Transcrição de áudio em tempo real
- Transcrição de arquivos de áudio (WAV, MP3, FLAC, OGG)
- Fine-tuning do modelo baseado no Wav2Vec2
- Exportação do modelo treinado

## Requisitos

- Python 3.7+
- Dependências listadas em `VoskRequirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/cassiusdbrito/FWsTrancri-o.git
cd FWsTrancri-o/Vosk
```

2. Instale as dependências:
```bash
pip install -r VoskRequirements.txt
```

3. Baixe um modelo Vosk:
- Acesse https://alphacephei.com/vosk/models
- Baixe o modelo desejado (recomendado: vosk-model-small-pt)
- Extraia o modelo na pasta `modelo-vosk`

## Uso

### Transcrição em Tempo Real
```bash
python transcricao_tempo_real.py
```

### Transcrição de Arquivo
```bash
python transcricao_arquivo.py
```

### Fine-tuning do Modelo
```bash
python fine_tuning.py
```

### Exportação do Modelo
```bash
python exportacao_modelo.py
```

## Estrutura do Projeto

- `transcricao_tempo_real.py`: Script para transcrição em tempo real
- `transcricao_arquivo.py`: Script para transcrição de arquivos de áudio
- `fine_tuning.py`: Script para fine-tuning do modelo
- `exportacao_modelo.py`: Script para exportar o modelo treinado
- `VoskRequirements.txt`: Lista de dependências do projeto

## Dataset para Fine-tuning

O dataset deve estar no formato JSON com a seguinte estrutura:
```json
{
    "audio_path": "caminho/para/audio.wav",
    "text": "transcrição do áudio"
}
```

Os arquivos devem ser organizados em:
- `dataset/train.json`: Dataset de treinamento
- `dataset/test.json`: Dataset de teste

## Logs

Os logs de fine-tuning e exportação são salvos no diretório `logs/`.

## Checkpoints

Os checkpoints do modelo são salvos no diretório `checkpoints/`.

## Licença

Este projeto está sob a licença MIT. 