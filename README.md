# FWS Transcriber

Um conjunto de ferramentas para transcrição de áudio usando diferentes modelos e APIs.

## Estrutura do Projeto

- **AssemblyAI**: Transcrição usando a API do AssemblyAI
- **Pocketsphinx**: Transcrição usando o modelo Pocketsphinx
- **Nvidia_NeMo**: Transcrição usando o modelo NeMo da NVIDIA
- **Whisper**: Transcrição usando o modelo Whisper da OpenAI
- **Vosk**: Transcrição usando o modelo Vosk

## Requisitos

Cada pasta tem seus próprios requisitos. Instale-os conforme necessário:

```bash
# AssemblyAI
pip install -r AssemblyAI/requirements.txt

# Pocketsphinx
pip install -r Pocketsphinx/requirements.txt

# Nvidia_NeMo
pip install -r Nvidia_NeMo/requirements.txt

# Whisper
pip install -r Whisper/WhisperRequirements.txt

# Vosk
pip install -r Vosk/requirements.txt
```

## Uso

Cada pasta contém um script de transcrição que pode ser executado independentemente:

```bash
# AssemblyAI
python AssemblyAI/assemblyTranscriber.py

# Pocketsphinx
python Pocketsphinx/pocketTranscriber.py

# Nvidia_NeMo
python Nvidia_NeMo/transcriberNeMo.py

# Whisper
python Whisper/transcricao_whisper.py

# Vosk
python Vosk/transcricao_vosk.py
```

## Observações

- Alguns modelos requerem o Microsoft Visual C++ Build Tools para instalação
- O FFmpeg é necessário para manipulação de áudio
- As chaves de API (como a do AssemblyAI) devem ser configuradas no código ou em variáveis de ambiente

