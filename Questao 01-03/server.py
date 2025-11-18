# server.py
import socket
from input_stream import PessoaInputStream

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("[SERVER] Aguardando conexão...")
    conn, addr = s.accept()
    print(f"[SERVER] Conectado com {addr}")

    with conn:
        inp = PessoaInputStream(conn.makefile("rb"))
        pessoas = inp.read_all()

        print("\n[SERVER] Pessoas recebidas:")
        for p in pessoas:
            print(f" - {p.nome} ({p.tipo()})")
