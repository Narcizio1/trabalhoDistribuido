#!/usr/bin/env python3
"""
Cliente de Votação (Questão 5) — recebe multicast e faz login/voto por TCP.
"""

import socket
import struct
import json
import threading
import time

MULTICAST_GROUP = ("224.1.1.1", 9999)
TCP_HOST = "localhost"
TCP_PORT = 6060

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("conexão encerrada")
        data += chunk
    return data

def listen_multicast():
    """Thread que escuta multicast e imprime mensagens."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        pass
    sock.bind(('', MULTICAST_GROUP[1]))
    mreq = socket.inet_aton(MULTICAST_GROUP[0]) + socket.inet_aton("0.0.0.0")
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print("[MULTICAST] Aguardando mensagens...")
    while True:
        data, addr = sock.recvfrom(4096)
        try:
            obj = json.loads(data.decode("utf-8"))
        except:
            print("[MULTICAST] Mensagem inválida")
            continue
        if obj.get("tipo") == "mensagem":
            print(f"\n📢 NOTIFICAÇÃO: {obj.get('texto')}\n")
        elif obj.get("tipo") == "resultado":
            print("\n📊 RESULTADO FINAL:")
            print(json.dumps(obj, indent=2, ensure_ascii=False))
            print()
        else:
            print("[MULTICAST] Recebido:", obj)

def run_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_HOST, TCP_PORT))
    except Exception as e:
        print("[ERRO] Não foi possível conectar ao servidor TCP:", e)
        return

    name = input("Seu nome (login): ").strip() or "anon"

    # send login
    login_b = json.dumps({"nome": name}).encode("utf-8")
    s.sendall(struct.pack("i", len(login_b)))
    s.sendall(login_b)

    # read candidates
    raw = recv_all(s, 4)
    size = struct.unpack("i", raw)[0]
    payload = recv_all(s, size).decode("utf-8")
    try:
        candidatos = json.loads(payload).get("candidatos", [])
    except:
        candidatos = []
    print("Candidatos disponíveis:", candidatos)

    voto = input("Digite o candidato para votar: ").strip()
    voto_b = json.dumps({"voto": voto}).encode("utf-8")
    s.sendall(struct.pack("i", len(voto_b)))
    s.sendall(voto_b)

    # read response
    raw = recv_all(s, 4)
    size = struct.unpack("i", raw)[0]
    payload = recv_all(s, size).decode("utf-8")
    resp = json.loads(payload)
    print("[SERVIDOR] Resposta:", resp.get("msg"))

    s.close()

if __name__ == "__main__":
    print("Cliente de votação iniciado.")
    t = threading.Thread(target=listen_multicast, daemon=True)
    t.start()
    time.sleep(0.1)
    run_client()
    # manter thread multicast viva até ctrl+c
    print("Cliente terminou a sessão TCP. Multicast continuará sendo exibido.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Saindo.")
