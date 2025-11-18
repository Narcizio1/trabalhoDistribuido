#!/usr/bin/env python3
# Questão 4 - Cliente TCP com serialização JSON

import socket
import struct
import json

HOST = "localhost"
PORT = 5050

pessoa = {
    "id": 1,
    "nome": "Matheus",
    "idade": 25,
    "sexo": "Masculino",
    "cpf": "12345678901"
}

def recv_all(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Conexão encerrada pelo servidor")
        data += chunk
    return data

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Serializa objeto Pessoa
    dados = json.dumps(pessoa).encode("utf-8")

    # Envia tamanho + conteúdo
    sock.sendall(struct.pack("i", len(dados)))
    sock.sendall(dados)
    print("[CLIENTE Q4] Dados enviados:", pessoa)

    # Recebe resposta
    raw_len = recv_all(sock, 4)
    tamanho = struct.unpack("i", raw_len)[0]
    resposta = json.loads(recv_all(sock, tamanho).decode("utf-8"))

    print("[CLIENTE Q4] Resposta recebida:", resposta)

    sock.close()

if __name__ == "__main__":
    main()
