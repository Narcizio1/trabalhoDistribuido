import socket
from modelos import Academia 
from servicos import cadastrar_aluno, cadastrar_instrutor, registrar_visitante, avaliar_desempenho 
from protocolo import RequestMessage, ReplyMessage 
from input_stream_rmi import receive_message 
from output_stream_rmi import send_message

HOST = "127.0.0.1"
PORT = 5000

academia_service = Academia("Gym Power RMI") 

METHOD_DISPATCHER = {
    "cadastrar_aluno": cadastrar_aluno,
    "cadastrar_instrutor": cadastrar_instrutor,
    "registrar_visitante": registrar_visitante,
    "avaliar_desempenho": avaliar_desempenho,
}

def get_request(stream):
    return receive_message(stream)

def send_reply(reply: ReplyMessage, stream):
    send_message(reply, stream)

# ----------------------------------------------------------------

def handle_request(request: RequestMessage, stream_out):
    method_id = request.method_id
    arguments = request.arguments 
    
    print(f"[SERVER] Recebida Req ID {request.request_id}: {method_id}")
    
    reply = None
    try:
        if request.object_reference.name != "AcademiaService":
            raise ValueError("Objeto Remoto Invalido.")

        funcao_local = METHOD_DISPATCHER.get(method_id)
        if not funcao_local:
            raise NotImplementedError(f"Metodo '{method_id}' nao implementado.")
        
        if method_id == "avaliar_desempenho":
             aluno_id = arguments.get('id')
             aluno = next((a for a in academia_service.alunos if a.id == aluno_id), None)
             if aluno:
                result = funcao_local(aluno)
             else:
                result = f"Aluno ID {aluno_id} nao encontrado para avaliacao."
        else:
            result = funcao_local(academia_service, **arguments)
            
        reply = ReplyMessage(request.request_id, result=result)
    
    except Exception as e:
        print(f"Erro na execucao: {type(e).__name__}: {e}")
        reply = ReplyMessage(request.request_id, exception=f"{type(e).__name__}: {str(e)}")
        
    finally:
        send_reply(reply, stream_out) 


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("[SERVER RMI] Aguardando conexao na porta 5000...")
        
        while True: 
            try:
                conn, addr = s.accept()
                print(f"[SERVER RMI] Conectado com {addr}")

                with conn:
                    stream_in = conn.makefile("rb")
                    stream_out = conn.makefile("wb")
                    
                    while True:
                        request = get_request(stream_in) 
                        if not request:
                            print(f"[SERVER RMI] Conexao com {addr} encerrada.")
                            break 
                        
                        handle_request(request, stream_out)
                        
            except KeyboardInterrupt:
                print("\n[SERVER RMI] Servidor encerrado.")
                break
            except Exception as e:
                print(f"[SERVER RMI] Erro inesperado: {type(e).__name__}: {e}")
                
if __name__ == "__main__":
    run_server()