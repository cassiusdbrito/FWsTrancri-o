# FWsTrancri-o

Sistema de transcrição de áudio usando CoquiSTT (STT - Speech-to-Text).

## Funcionalidades

- Transcrição de áudio em tempo real
- Transcrição de arquivos de áudio (WAV, MP3, FLAC, OGG)
- Treinamento de modelo personalizado
- Exportação de modelo treinado

## Requisitos

- Python 3.7+
- Dependências listadas em `CoquiRequirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/cassiusdbrito/FWsTrancri-o.git
cd FWsTrancri-o/CoquiSTT
```

2. Instale as dependências:
```bash
pip install -r CoquiRequirements.txt
```

## Uso

### Transcrição em Tempo Real
```bash
python transcricao_tempo_real.py
```

### Transcrição de Arquivo
```bash
python transcricao_arquivo.py
```

### Treinamento do Modelo
```bash
python treinamento_modelo.py
```

### Exportação do Modelo
```bash
python exportacao_modelo.py
```

## Estrutura do Projeto

- `transcricao_tempo_real.py`: Script para transcrição em tempo real
- `transcricao_arquivo.py`: Script para transcrição de arquivos de áudio
- `treinamento_modelo.py`: Script para treinar o modelo
- `exportacao_modelo.py`: Script para exportar o modelo treinado
- `CoquiRequirements.txt`: Lista de dependências do projeto

## Logs

Os logs de treinamento e exportação são salvos no diretório `logs/`.

## Checkpoints

Os checkpoints do modelo são salvos no diretório `checkpoints/`.

## Licença

Este projeto está sob a licença MIT. 