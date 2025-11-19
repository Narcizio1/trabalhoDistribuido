import struct
from protocolo import Message

def receive_message(origem_stream) -> Message:
    try:
        raw_size = origem_stream.read(4)
        if not raw_size:
            return None 
        
        tamanho = struct.unpack("i", raw_size)[0]
    except struct.error:
        return None
    
    data_bytes = origem_stream.read(tamanho)
    
    if len(data_bytes) < tamanho:
        return None

    return Message.from_bytes(data_bytes)