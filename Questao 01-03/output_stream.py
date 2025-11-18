# output_stream.py
import struct
from modelos import Pessoa

class PessoaOutputStream:
    """
    Envia um conjunto de objetos Pessoa (e subclasses)
    para um fluxo binário (stdout, arquivo ou socket).
    """

    def __init__(self, pessoas, quantidade, num_bytes_atributos, destino_stream):
        self.pessoas = pessoas
        self.quantidade = quantidade
        self.num_bytes_atributos = num_bytes_atributos
        self.destino_stream = destino_stream  # Deve ser modo binário

    def write_all(self):
        for p in self.pessoas[:self.quantidade]:
            tipo_b = p.tipo().encode("utf-8")
            nome_b = p.nome.encode("utf-8")

            data = (
                struct.pack("i", len(tipo_b)) + tipo_b +
                struct.pack("i", p.id) +
                struct.pack("i", p.idade) +
                struct.pack("i", len(nome_b)) + nome_b
            )

            # Tamanho total do bloco
            self.destino_stream.write(struct.pack("i", len(data)))

            # Dados
            self.destino_stream.write(data)
