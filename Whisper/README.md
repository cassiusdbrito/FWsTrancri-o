# FWsTrancri-o Whisper

Sistema de transcrição de áudio usando OpenAI Whisper.

## Funcionalidades

- Transcrição de arquivos de áudio (WAV, M4A, OGG)
- Conversão automática de formatos de áudio
- Suporte a transcrição de pastas inteiras
- Logging detalhado das operações

## Requisitos

- Python 3.7+
- Dependências listadas em `WhisperRequirements.txt`
- FFmpeg instalado no sistema

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/cassiusdbrito/FWsTrancri-o.git
cd FWsTrancri-o/Whisper
```

2. Instale as dependências:
```bash
pip install -r WhisperRequirements.txt
```

3. Instale o FFmpeg:
- Windows: Baixe de https://ffmpeg.org/download.html
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

4. Baixe o modelo Whisper:
- Acesse https://huggingface.co/openai/whisper-base
- Baixe o modelo desejado (recomendado: tiny.pt)
- Coloque o arquivo na pasta `modelo/`

## Uso

### Transcrição de Arquivo Único
```python
from transcricao_whisper import TranscricaoWhisper

transcricao = TranscricaoWhisper()
resultado = transcricao.transcrever("audio.m4a")
print(resultado["text"])
```

### Transcrição de Pasta
```python
from transcricao_whisper import TranscricaoWhisper

transcricao = TranscricaoWhisper()
resultados = transcricao.transcrever_pasta("pasta_audios")
for arquivo, resultado in resultados.items():
    print(f"\nTranscrição de {arquivo}:")
    print(resultado["text"])
```

## Estrutura do Projeto

- `transcricao_whisper.py`: Script principal de transcrição
- `testes.py`: Testes unitários
- `WhisperRequirements.txt`: Lista de dependências
- `modelo/`: Pasta para armazenar o modelo Whisper
- `audios_transformados/`: Pasta para arquivos convertidos
- `logs/`: Pasta para arquivos de log

## Logs

Os logs são salvos no diretório `logs/` com timestamp.

## Formatos Suportados

- Entrada: WAV, M4A, OGG
- Saída: WAV (conversão automática)

## Licença

Este projeto está sob a licença MIT. 