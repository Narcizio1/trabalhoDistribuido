# Trabalho 02 - Remote Method Invocation (RMI)

## Equipe

-   Matheus Narcizio (494693)
-   Maria Davila (586054)

## Instruções

Após configurar o ambiente Python e instalar as dependências (se
houver), basta iniciar o **servidor RMI** com:

``` bash
python server_rmi.py
```

O servidor ficará escutando em:

    127.0.0.1:5000

Em seguida, execute o **cliente RMI** com:

``` bash
python client_rmi.py
```

O cliente realizará automaticamente as requisições remotas exigidas pelo
trabalho.

------------------------------------------------------------------------

## Arquitetura

O sistema implementa a Questão 1 do Trabalho 1 usando **RMI
customizado**, baseado no protocolo **requisição--resposta** do livro
texto.

As mensagens trafegadas seguem o formato:

-   message_type\
-   request_id\
-   object_reference\
-   method_id\
-   arguments (Base64 JSON)\
-   result ou exception

Toda a representação externa de dados é feita com **JSON + Base64**,
conforme permitido no enunciado.

------------------------------------------------------------------------

## Estrutura do Projeto

    📁 projeto
     ├── main.py
     ├── client_rmi.py
     ├── server_rmi.py
     ├── protocolo.py
     ├── input_stream_rmi.py
     ├── output_stream_rmi.py
     ├── servicos.py
     ├── modelos.py
     ├── persistencia.py
     └── dados_academia.json

------------------------------------------------------------------------

## Objetos do Sistema

O trabalho exige **mínimo de 4 entidades**, com **2 extensões** e **2
agregações**.

### ✔ Entidades

-   Pessoa
-   Aluno
-   Instrutor
-   Funcionario
-   Visitante
-   Academia

### ✔ Extensões (Herança "é-um")

-   Aluno → Pessoa
-   Instrutor → Pessoa
-   Funcionario → Pessoa
-   Visitante → Pessoa

### ✔ Agregações ("tem-um")

-   A classe Academia possui listas de:
    -   alunos
    -   instrutores
    -   funcionários
    -   visitantes
-   A classe Aluno possui lista de treinos, cada treino possui
    exercícios

------------------------------------------------------------------------

## Serviços Remotos (RMI)

O servidor expõe **4 métodos remotos**, atendendo ao requisito mínimo:

-   cadastrar_aluno
-   cadastrar_instrutor
-   registrar_visitante
-   avaliar_desempenho

Cada chamada remota: 1. Recebe parâmetros por **valor** (JSON
codificado). 2. Identifica o objeto remoto via **RemoteObjectRef**
(passagem por referência). 3. Executa o método no servidor. 4. Retorna o
resultado empacotado.

------------------------------------------------------------------------

## Execução do Cliente

Ao rodar `client_rmi.py`, são realizadas automaticamente 4 chamadas
remotas:

1.  Cadastro de aluno\
2.  Cadastro de instrutor\
3.  Registro de visitante\
4.  Avaliação de desempenho

Exemplo de saída:

    [CLIENT] Enviada Req ID 1: cadastrar_aluno
    ✅ RMI Sucesso: Leo RMI (Aluno)

    [CLIENT] Enviada Req ID 4: avaliar_desempenho
    Aluno Leo possui X treinos cadastrados.

------------------------------------------------------------------------

## Back-end (Servidor RMI)

O servidor processa as requisições através das funções:

-   get_request() -- desempacota solicitações
-   handle_request() -- executa o método remoto
-   send_reply() -- empacota respostas

O dispatcher dos métodos é:

``` python
METHOD_DISPATCHER = {
    "cadastrar_aluno": cadastrar_aluno,
    "cadastrar_instrutor": cadastrar_instrutor,
    "registrar_visitante": registrar_visitante,
    "avaliar_desempenho": avaliar_desempenho,
}
```

------------------------------------------------------------------------

## Representação Externa dos Dados

Conforme especificado no Trabalho 2:

-   A comunicação remota utiliza **JSON como formato externo**.\
-   O conteúdo JSON é **codificado em Base64** antes de ser enviado.\
-   Tanto requisições como respostas seguem essa mesma estrutura.

Implementação em `protocolo.py`:

-   Message.to_bytes()
-   Message.from_bytes()

------------------------------------------------------------------------
