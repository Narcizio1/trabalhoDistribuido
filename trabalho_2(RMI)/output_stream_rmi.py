import struct
from protocolo import RequestMessage, ReplyMessage

def send_message(message: RequestMessage or ReplyMessage, destino_stream):
    
    data_bytes = message.to_bytes() 

    destino_stream.write(struct.pack("i", len(data_bytes)))

    destino_stream.write(data_bytes)
    destino_stream.flush()