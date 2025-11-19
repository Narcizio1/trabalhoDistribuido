import socket
from protocolo import RequestMessage, RemoteObjectRef
from input_stream_rmi import receive_message 
from output_stream_rmi import send_message 

HOST = "127.0.0.1"
PORT = 5000
request_counter = 1 

def do_operation(obj_ref: RemoteObjectRef, method_id: str, arguments: dict, stream_out, stream_in):

    global request_counter
    
    request = RequestMessage(
        request_id=request_counter,
        object_reference=obj_ref, 
        method_id=method_id,
        arguments=arguments 
    )
    current_request_id = request_counter
    request_counter += 1

    send_message(request, stream_out)
    print(f"\n[CLIENT] Enviada Req ID {current_request_id}: {method_id} com args: {arguments}")

    reply = receive_message(stream_in)
    
    if reply is None:
        raise ConnectionError("Conexao perdida ou resposta invalida.")
    
    if reply.exception:
        print(f"Erro no Servidor (Req ID {current_request_id}): {reply.exception}")
        return None
        
    return reply.result

def run_client():
    obj_ref = RemoteObjectRef("AcademiaService")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("[CLIENT RMI] Conectado ao servidor.")
            
            stream_out = s.makefile("wb") 
            stream_in = s.makefile("rb")  

            print("--- Executando 4 Chamadas Remotas (RMI) ---")

            args_aluno = {"id": 100, "nome": "Leo RMI", "idade": 30, "sexo": "M"}
            result = do_operation(obj_ref, "cadastrar_aluno", args_aluno, stream_out, stream_in)
            if result:
                print(f"RMI Sucesso (cadastrar_aluno): {result.get('nome')} ({result.get('tipo')})")

            args_instrutor = {"id": 200, "nome": "Pat RMI", "idade": 25, "sexo": "F", "especialidade": "Yoga"}
            result = do_operation(obj_ref, "cadastrar_instrutor", args_instrutor, stream_out, stream_in)
            if result:
                print(f"RMI Sucesso (cadastrar_instrutor): {result.get('nome')} ({result.get('tipo')}) Especialidade: {result.get('especialidade')}")

            args_visitante = {"id": 300, "nome": "Visitante RMI", "idade": 40, "sexo": "M"}
            result = do_operation(obj_ref, "registrar_visitante", args_visitante, stream_out, stream_in)
            if result:
                print(f"RMI Sucesso (registrar_visitante): {result.get('nome')} ({result.get('tipo')})")

            args_avaliar = {"id": 100} 
            result = do_operation(obj_ref, "avaliar_desempenho", args_avaliar, stream_out, stream_in)
            if result:
                print(f"RMI Sucesso (avaliar_desempenho): {result}")
            
            print("\n--- Fim das Chamadas RMI ---")

        except ConnectionRefusedError:
            print("\nERRO: Não foi possível conectar. Certifique-se de que o servidor (server_rmi.py) está em execução.")
        except Exception as e:
            print(f"\nERRO Inesperado no Cliente: {type(e).__name__}: {e}")
            
if __name__ == "__main__":
    run_client()