"""
Model que representa um Exame no sistema.
"""

from dataclasses import dataclass


@dataclass
class Exame:

    def __init__(self, id, arquivo, resumo, data_upload, categoria):

        self.id = id
        self.arquivo = arquivo
        self.resumo = resumo
        self.data_upload = data_upload
        self.categoria = categoria

