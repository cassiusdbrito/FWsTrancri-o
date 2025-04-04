import unittest
import os
import shutil
import ffmpeg
from transcricao_whisper import whisper_transcrição

class TestWhisper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes"""
        # Caminho do arquivo de áudio existente
        cls.arquivo_audio = "C:\\Users\\cassi\\fwsTransc\\Áudios\\audio_zap.wav"

    def test_transcricao_whisper(self):
        """Testa a transcrição de um arquivo usando Whisper"""
        resultado = whisper_transcrição(self.arquivo_audio)
        self.assertIsNotNone(resultado)
        self.assertIn("text", resultado)
        self.assertIn("segments", resultado)
        print("\nTranscrição:", resultado["text"])

if __name__ == "__main__":
    unittest.main()