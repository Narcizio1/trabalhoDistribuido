import json
from modelos import Aluno, Instrutor, Funcionario, Visitante

def carregar_dados(academia, arquivo="dados_academia.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        for a in dados["alunos"]:
            academia.alunos.append(Aluno(a["id"], a["nome"], a["idade"], a["sexo"], a["plano_treino"]))

        for i in dados["instrutores"]:
            academia.instrutores.append(Instrutor(i["id"], i["nome"], i["idade"], i["sexo"], i["especialidade"]))

        for f in dados["funcionarios"]:
            academia.funcionarios.append(Funcionario(f["id"], f["nome"], f["idade"], f["sexo"], f["cargo"]))

        for v in dados["visitantes"]:
            academia.visitantes.append(Visitante(v["id"], v["nome"], v["idade"], v["sexo"]))

        print("[JSON] Dados carregados com sucesso.")

    except FileNotFoundError:
        print("[AVISO] Nenhum arquivo JSON encontrado. Começando vazio.")


def salvar_dados(academia, arquivo="dados_academia.json"):
    dados = {
        "alunos": [
            {"id": a.id, "nome": a.nome, "idade": a.idade, "sexo": a.sexo, "plano_treino": a.plano_treino}
            for a in academia.alunos
        ],
        "instrutores": [
            {"id": i.id, "nome": i.nome, "idade": i.idade, "sexo": i.sexo, "especialidade": i.especialidade}
            for i in academia.instrutores
        ],
        "funcionarios": [
            {"id": f.id, "nome": f.nome, "idade": f.idade, "sexo": f.sexo, "cargo": f.cargo}
            for f in academia.funcionarios
        ],
        "visitantes": [
            {"id": v.id, "nome": v.nome, "idade": v.idade, "sexo": v.sexo}
            for v in academia.visitantes
        ]
    }

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("[JSON] Dados salvos com sucesso.")
