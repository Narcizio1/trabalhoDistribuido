import sys
from modelos import Academia
from servicos import (
    cadastrar_aluno, cadastrar_instrutor, cadastrar_funcionario, registrar_visitante,
    criar_treino, adicionar_exercicio, atualizar_treino, avaliar_desempenho
)
from persistencia import carregar_dados, salvar_dados
def menu():
    print("\n===== SISTEMA DE ACADEMIA =====")
    print("1  - Cadastrar Aluno")
    print("2  - Cadastrar Instrutor")
    print("3  - Cadastrar Funcionário")
    print("4  - Registrar Visitante")
    print("5  - Criar Treino para Aluno")
    print("6  - Adicionar Exercício ao Treino")
    print("7  - Atualizar Treino do Aluno")
    print("8  - Avaliar Desempenho do Aluno")
    print("9  - Listar Pessoas da Academia")
    print("10 - Listar treinos de um aluno")
    print("0  - Sair")
    return input("Escolha: ").strip()

def selecionar_aluno(academia):
    if not academia.alunos:
        print("\nNenhum aluno cadastrado.")
        return None
    print("\n--- Alunos Cadastrados ---")
    for a in academia.alunos:
        print(f"{a.id} - {a.nome}")
    try:
        id_escolhido = int(input("ID: ").strip())
    except:
        print("ID inválido.")
        return None
    for a in academia.alunos:
        if a.id == id_escolhido:
            return a
    print("Aluno não encontrado.")
    return None

def buscar_aluno_por_id_ou_nome(academia, termo):
    termo = termo.strip()
    try:
        id_busca = int(termo)
        for a in academia.alunos:
            if a.id == id_busca: return a
    except:
        pass
    termo = termo.lower()
    for a in academia.alunos:
        if termo in a.nome.lower(): return a
    return None

def listar_treinos_do_aluno(academia):
    busca = input("\nID ou nome do aluno: ").strip()
    aluno = buscar_aluno_por_id_ou_nome(academia, busca)
    if not aluno:
        print("Aluno não encontrado.")
        return
    print(f"\nTreinos de {aluno.nome}:")
    if not aluno.plano_treino:
        print("Nenhum treino cadastrado.")
        return
    for treino in aluno.plano_treino:
        print(f"\n🏋️ {treino['nome']}:")
        for ex in treino["exercicios"]:
            print(f" - {ex}")

def main():
    academia = Academia("Gym Power")
    carregar_dados(academia)
    print("\n🏋️ Sistema iniciado!")

    while True:
        opc = menu()

        if opc == "1":
            cadastrar_aluno(academia, int(input("ID: ")), input("Nome: "), int(input("Idade: ")), input("Sexo: "))
            print("Aluno cadastrado!")

        elif opc == "2":
            cadastrar_instrutor(academia, int(input("ID: ")), input("Nome: "), int(input("Idade: ")), input("Sexo: "), input("Especialidade: "))
            print("Instrutor cadastrado!")

        elif opc == "3":
            cadastrar_funcionario(academia, int(input("ID: ")), input("Nome: "), int(input("Idade: ")), input("Sexo: "), input("Cargo: "))
            print("Funcionário cadastrado!")

        elif opc == "4":
            registrar_visitante(academia, int(input("ID: ")), input("Nome: "), int(input("Idade: ")), input("Sexo: "))
            print("Visitante registrado!")

        elif opc == "5":
            aluno = selecionar_aluno(academia)
            if aluno:
                criar_treino(aluno, input("Nome do treino: "))
                print("Treino criado!")

        elif opc == "6":
            aluno = selecionar_aluno(academia)
            if aluno:
                adicionar_exercicio(aluno, input("Treino: "), input("Exercício: "))
                print("Exercício adicionado!")

        elif opc == "7":
            aluno = selecionar_aluno(academia)
            if aluno:
                atualizar_treino(aluno, input("Treino: "), [x.strip() for x in input("Exercícios (vírgula): ").split(",")])
                print("Treino atualizado!")

        elif opc == "8":
            aluno = selecionar_aluno(academia)
            if aluno:
                print(avaliar_desempenho(aluno))

        elif opc == "9":
            print("\n--- Pessoas na Academia ---")
            for lista in (academia.alunos, academia.instrutores, academia.funcionarios, academia.visitantes):
                for p in lista:
                    print(" -", p.nome)

        elif opc == "10":
            listar_treinos_do_aluno(academia)

        elif opc == "0":
            salvar_dados(academia)
            print("\nSaindo... Dados salvos!")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()