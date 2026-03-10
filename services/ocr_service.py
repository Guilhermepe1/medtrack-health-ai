"""
Service responsável por OCR (extração de texto de imagens).
"""

import pytesseract
from PIL import Image

# Caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Guilherme\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def extrair_texto_imagem(arquivo):

    imagem = Image.open(arquivo)

    texto = pytesseract.image_to_string(imagem)

    return texto
