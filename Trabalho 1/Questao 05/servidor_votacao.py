#!/usr/bin/env python3
"""
Servidor de Votação (Questão 5) - JSON, TCP (login/voto), UDP multicast (mensagens/resultado).
Admin local no console pode: add <cand>, remove <cand>, msg <texto>, start <segundos>, end, status, exit
"""

import socket
import struct
import json
import threading
import time
import sys

MULTICAST_GROUP = ("224.1.1.1", 9999)
TCP_HOST = "localhost"
TCP_PORT = 6060

lock = threading.Lock()
candidates = {}        # {"nome": votos}
voting_open = False
voting_end_time = None
voting_duration = 60   # default seconds
server_running = True

def send_multicast(obj):
    """Envia um objeto (dicionário) via multicast UDP como JSON."""
    data = json.dumps(obj).encode("utf-8")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        # TTL pequeno
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(data, MULTICAST_GROUP)
    finally:
        sock.close()

def announce(msg_text):
    """Envia mensagem administrativa via multicast."""
    obj = {"tipo": "mensagem", "texto": msg_text, "ts": time.time()}
    send_multicast(obj)
    print("[ADMIN] Mensagem multicast enviada.")

def announce_results():
    """Calcula resultados e envia via multicast."""
    with lock:
        total = sum(candidates.values())
        if total > 0:
            winner = max(candidates.items(), key=lambda kv: kv[1])[0]
        else:
            winner = None
        percent = {c: (f"{(v/total*100):.2f}%" if total>0 else "0.00%") for c, v in candidates.items()}

    obj = {
        "tipo": "resultado",
        "total_votos": total,
        "vencedor": winner,
        "percentuais": percent,
        "detalhes": candidates,
        "ts": time.time()
    }
    send_multicast(obj)
    print("[VOTAÇÃO] Resultado enviado via multicast.")

def close_voting():
    global voting_open
    with lock:
        voting_open = False
    print("[VOTAÇÃO] Encerrada.")
    announce_results()

def voting_timer(duration):
    global voting_end_time
    voting_end_time = time.time() + duration
    print(f"[VOTAÇÃO] Iniciada por {duration} segundos (até {time.ctime(voting_end_time)}).")
    while True:
        if not voting_open:
            break
        if time.time() >= voting_end_time:
            close_voting()
            break
        time.sleep(1)

def handle_client(conn, addr):
    """Thread por cliente TCP — faz login, envia lista, recebe voto e responde (tudo em JSON com length prefix)."""
    try:
        # read size then payload helper
        def recv_all(n):
            data = b''
            while len(data) < n:
                chunk = conn.recv(n - len(data))
                if not chunk:
                    raise ConnectionError("Conexão encerrada pelo cliente")
                data += chunk
            return data

        # Recebe login
        raw = recv_all(4)
        size = struct.unpack("i", raw)[0]
        payload = recv_all(size).decode("utf-8")
        login = json.loads(payload)
        nome = login.get("nome", "anon")
        print(f"[TCP] Login de {nome} de {addr}")

        # Envia lista de candidatos
        with lock:
            lista = list(candidates.keys())
        reply = {"candidatos": lista}
        reply_b = json.dumps(reply).encode("utf-8")
        conn.sendall(struct.pack("i", len(reply_b)))
        conn.sendall(reply_b)

        # Recebe voto
        raw = recv_all(4)
        size = struct.unpack("i", raw)[0]
        payload = recv_all(size).decode("utf-8")
        voto_obj = json.loads(payload)
        voto = voto_obj.get("voto")

        resposta = {"status": "erro", "msg": ""}

        with lock:
            if not voting_open:
                resposta["msg"] = "Votação encerrada."
            elif voto not in candidates:
                resposta["msg"] = "Candidato inválido."
            else:
                candidates[voto] += 1
                resposta = {"status": "ok", "msg": f"Voto em '{voto}' registrado."}
                print(f"[VOTO] {nome} -> {voto}")

        resp_b = json.dumps(resposta).encode("utf-8")
        conn.sendall(struct.pack("i", len(resp_b)))
        conn.sendall(resp_b)

    except Exception as e:
        print(f"[ERRO] Cliente {addr}: {e}")
    finally:
        conn.close()

def start_tcp_server():
    global server_running
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((TCP_HOST, TCP_PORT))
    srv.listen(5)
    print(f"[TCP] Servidor de votação ouvindo em {TCP_HOST}:{TCP_PORT}")
    while server_running:
        try:
            conn, addr = srv.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
        except Exception as e:
            print(f"[ERRO] accept(): {e}")
            break
    srv.close()

def admin_console():
    """Interface simples via console para o admin local."""
    global voting_open, voting_duration
    help_text = (
        "Comandos admin:\n"
        "  add <nome>       - adiciona candidato\n"
        "  remove <nome>    - remove candidato\n"
        "  list             - mostra candidatos e votos\n"
        "  msg <texto>      - envia mensagem multicast\n"
        "  start <segundos> - inicia votação (tempo em seg)\n"
        "  end              - encerra votação agora\n"
        "  status           - mostra status da votação\n"
        "  exit             - encerra servidor\n"
    )
    print(help_text)
    while True:
        try:
            cmd = input("admin> ").strip()
        except EOFError:
            cmd = "exit"
        if not cmd:
            continue
        parts = cmd.split(" ", 1)
        op = parts[0].lower()

        if op == "add" and len(parts) > 1:
            name = parts[1].strip()
            with lock:
                if name in candidates:
                    print("[ADMIN] Candidato já existe.")
                else:
                    candidates[name] = 0
                    print(f"[ADMIN] Candidato '{name}' adicionado.")
        elif op == "remove" and len(parts) > 1:
            name = parts[1].strip()
            with lock:
                if name in candidates:
                    del candidates[name]
                    print(f"[ADMIN] Candidato '{name}' removido.")
                else:
                    print("[ADMIN] Candidato não existe.")
        elif op == "list":
            with lock:
                print("Candidatos e votos:", candidates)
        elif op == "msg" and len(parts) > 1:
            announce(parts[1].strip())
        elif op == "start":
            arg = parts[1].strip() if len(parts)>1 else ""
            try:
                sec = int(arg) if arg else voting_duration
            except:
                print("[ADMIN] start <segundos>")
                continue
            with lock:
                if voting_open:
                    print("[ADMIN] Votação já está aberta.")
                else:
                    voting_open = True
                    t = threading.Thread(target=voting_timer, args=(sec,), daemon=True)
                    t.start()
        elif op == "end":
            with lock:
                if voting_open:
                    close_voting()
                else:
                    print("[ADMIN] Votação já está encerrada.")
        elif op == "status":
            with lock:
                print("Votação aberta:", voting_open)
                print("Candidatos:", candidates)
                if voting_open and voting_end_time:
                    print("Termina em:", time.ctime(voting_end_time))
        elif op == "exit":
            print("[ADMIN] Encerrando servidor...")
            with lock:
                # before exit, send results if voting open
                if voting_open:
                    close_voting()
            # stop server loop
            global server_running
            server_running = False
            # also send a multicast notice
            announce("Servidor encerrando.")
            break
        else:
            print(help_text)

def main():
    print("Servidor de Votação (JSON) iniciado.")
    # pre-popula alguns candidatos
    with lock:
        candidates.update({"A": 0, "B": 0, "C": 0})

    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()

    admin_console()

    print("Servidor finalizado.")
    sys.exit(0)

if __name__ == "__main__":
    main()
