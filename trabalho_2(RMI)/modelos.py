class Pessoa:
    def __init__(self, id, nome, idade, sexo):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.sexo = sexo

    def tipo(self):
        return "Pessoa"


class Aluno(Pessoa):
    def __init__(self, id, nome, idade, sexo, plano_treino=None):
        super().__init__(id, nome, idade, sexo)
        self.plano_treino = plano_treino or []

    def tipo(self):
        return "Aluno"


class Instrutor(Pessoa):
    def __init__(self, id, nome, idade, sexo, especialidade):
        super().__init__(id, nome, idade, sexo)
        self.especialidade = especialidade

    def tipo(self):
        return "Instrutor"


class Funcionario(Pessoa):
    def __init__(self, id, nome, idade, sexo, cargo):
        super().__init__(id, nome, idade, sexo)
        self.cargo = cargo

    def tipo(self):
        return "Funcionario"


class Visitante(Pessoa):
    def tipo(self):
        return "Visitante"


class Academia:
    def __init__(self, nome):
        self.nome = nome
        self.alunos = []
        self.instrutores = []
        self.funcionarios = []
        self.visitantes = []

    def __str__(self):
        return f"Academia: {self.nome} | Alunos: {len(self.alunos)} | Instrutores: {len(self.instrutores)}"
