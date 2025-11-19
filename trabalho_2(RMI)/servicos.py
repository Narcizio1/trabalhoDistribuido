from modelos import Aluno, Instrutor, Funcionario, Visitante

# ------------------ CADASTROS ------------------

def cadastrar_aluno(academia, id, nome, idade, sexo):
    aluno = Aluno(id, nome, idade, sexo, plano_treino=[])
    academia.alunos.append(aluno)
    return aluno


def cadastrar_instrutor(academia, id, nome, idade, sexo, especialidade):
    instrutor = Instrutor(id, nome, idade, sexo, especialidade)
    academia.instrutores.append(instrutor)
    return instrutor


def cadastrar_funcionario(academia, id, nome, idade, sexo, cargo):
    funcionario = Funcionario(id, nome, idade, sexo, cargo)
    academia.funcionarios.append(funcionario)
    return funcionario


def registrar_visitante(academia, id, nome, idade, sexo):
    visitante = Visitante(id, nome, idade, sexo)
    academia.visitantes.append(visitante)
    return visitante


# ------------------ TREINOS ------------------

def criar_treino(aluno, nome_treino):
    if aluno.plano_treino is None or not isinstance(aluno.plano_treino, list):
        aluno.plano_treino = []

    aluno.plano_treino.append({
        "nome": nome_treino,
        "exercicios": []
    })


def adicionar_exercicio(aluno, nome_treino, exercicio):
    for treino in aluno.plano_treino:
        if treino.get("nome", "").lower() == nome_treino.lower():
            treino["exercicios"].append(exercicio)
            return
    print("Treino não encontrado.")


def atualizar_treino(aluno, nome_treino, nova_lista_exercicios):
    for treino in aluno.plano_treino:
        if treino.get("nome", "").lower() == nome_treino.lower():
            treino["exercicios"] = nova_lista_exercicios
            return
    print("Treino não encontrado.")


def avaliar_desempenho(aluno):
    if not aluno.plano_treino:
        return f"{aluno.nome} ainda não possui treinos cadastrados."
    total_exercicios = sum(len(t["exercicios"]) for t in aluno.plano_treino)
    return f"{aluno.nome} possui {len(aluno.plano_treino)} treinos com {total_exercicios} exercícios registrados."
