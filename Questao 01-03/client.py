# client.py
import socket
from modelos import Academia
from persistencia import carregar_dados
from output_stream import PessoaOutputStream

HOST = "127.0.0.1"
PORT = 5000

academia = Academia("Gym Power")
carregar_dados(academia)

pessoas = (
    academia.alunos +
    academia.instrutores +
    academia.funcionarios +
    academia.visitantes
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[CLIENT] Conectado ao servidor.")

    out = PessoaOutputStream(
        pessoas=pessoas,
        quantidade=len(pessoas),
        num_bytes_atributos=64,
        destino_stream=s.makefile("wb")
    )

    out.write_all()
    print(f"[CLIENT] Enviadas {len(pessoas)} pessoas.")
