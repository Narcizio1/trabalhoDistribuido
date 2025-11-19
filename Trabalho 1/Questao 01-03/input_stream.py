# input_stream.py
import struct
from modelos import Aluno, Instrutor, Funcionario, Visitante

class PessoaInputStream:
    """
    Reconstrói objetos Pessoa a partir de um fluxo binário.
    """

    def __init__(self, origem_stream):
        self.origem_stream = origem_stream  # Deve ser modo binário

    def read_all(self):
        pessoas = []

        while True:
            raw = self.origem_stream.read(4)
            if not raw:
                break

            tamanho = struct.unpack("i", raw)[0]
            data = self.origem_stream.read(tamanho)

            offset = 0

            tipo_len = struct.unpack("i", data[offset:offset+4])[0]
            offset += 4
            tipo = data[offset:offset+tipo_len].decode("utf-8")
            offset += tipo_len

            id = struct.unpack("i", data[offset:offset+4])[0]
            offset += 4

            idade = struct.unpack("i", data[offset:offset+4])[0]
            offset += 4

            nome_len = struct.unpack("i", data[offset:offset+4])[0]
            offset += 4
            nome = data[offset:offset+nome_len].decode("utf-8")

            if tipo == "Aluno":
                pessoa = Aluno(id, nome, idade, "?")
            elif tipo == "Instrutor":
                pessoa = Instrutor(id, nome, idade, "?", "Especialidade não enviada")
            elif tipo == "Funcionario":
                pessoa = Funcionario(id, nome, idade, "?", "Cargo não enviado")
            else:
                pessoa = Visitante(id, nome, idade, "?")

            pessoas.append(pessoa)

        return pessoas
