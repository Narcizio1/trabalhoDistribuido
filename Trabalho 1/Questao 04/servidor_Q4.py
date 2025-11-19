#!/usr/bin/env python3
# Questão 4 - Servidor TCP com serialização JSON

import socket
import struct
import json

HOST = "localhost"
PORT = 5050

def recv_all(conn, n):
    """Recebe exatamente n bytes"""
    data = b""
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Conexão encerrada pelo cliente")
        data += chunk
    return data

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[SERVIDOR Q4] Aguardando conexões em {HOST}:{PORT} ...")

    while True:
        conn, addr = server.accept()
        print(f"[SERVIDOR Q4] Conectado a {addr}")

        try:
            # Recebe tamanho + dados JSON
            raw_len = recv_all(conn, 4)
            tamanho = struct.unpack("i", raw_len)[0]
            dados_json = recv_all(conn, tamanho).decode("utf-8")

            pessoa = json.loads(dados_json)
            print(f"[SERVIDOR Q4] Recebido objeto: {pessoa}")

            # Cria resposta
            resposta = {"status": "ok", "mensagem": f"Dados de {pessoa['nome']} recebidos com sucesso!"}
            resp_bytes = json.dumps(resposta).encode("utf-8")

            # Envia tamanho + dados
            conn.sendall(struct.pack("i", len(resp_bytes)))
            conn.sendall(resp_bytes)

        except Exception as e:
            print(f"[ERRO] {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
