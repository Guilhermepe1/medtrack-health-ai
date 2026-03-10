"""
Utilitários para manipulação de datas.
"""

from datetime import datetime


def extrair_ano(data_string):
    """
    Extrai o ano de uma data no formato string.
    """

    data = datetime.fromisoformat(data_string)

    return data.year


def formatar_data(data_string):
    """
    Converte data ISO para formato amigável.
    """

    data = datetime.fromisoformat(data_string)

    return data.strftime("%d/%m/%Y %H:%M")
