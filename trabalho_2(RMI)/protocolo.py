import json
import base64
from typing import Any, Dict

TYPE_REQUEST = 0
TYPE_REPLY = 1

def obj_to_dict(obj):
    if hasattr(obj, 'id') and hasattr(obj, 'nome') and hasattr(obj, 'tipo'):
        data = {
            "id": obj.id,
            "nome": obj.nome,
            "idade": obj.idade,
            "sexo": obj.sexo,
            "tipo": obj.tipo()
        }
        if data["tipo"] == "Aluno":
            data["plano_treino"] = obj.plano_treino if obj.plano_treino is not None else []
        elif data["tipo"] == "Instrutor":
            data["especialidade"] = obj.especialidade
        elif data["tipo"] == "Funcionario":
            data["cargo"] = obj.cargo
        return data
    return obj

class RemoteObjectRef:
    def __init__(self, name="AcademiaService"):
        self.name = name

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data: dict):
        return RemoteObjectRef(data.get("name"))

class Message:
    def __init__(self, message_type: int, request_id: int):
        self.message_type = message_type
        self.request_id = request_id

    def to_bytes(self) -> bytes:
        data = self.__dict__.copy()

        if 'object_reference' in data and data['object_reference'] is not None:
            data['object_reference'] = data['object_reference'].to_dict()

        data_field = data.get('arguments') or data.get('result')

        if data_field is not None:
            field_name = 'arguments' if self.message_type == TYPE_REQUEST else 'result'
            
            data_to_serialize = data_field
            if field_name == 'result':
                data_to_serialize = obj_to_dict(data_field)
            
            payload_json = json.dumps(data_to_serialize)
            
            data[field_name] = base64.b64encode(payload_json.encode('utf-8')).decode('utf-8')

        return json.dumps(data).encode('utf-8')

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Message':
        data_dict = json.loads(data.decode('utf-8'))

        if 'object_reference' in data_dict and data_dict['object_reference'] is not None:
            data_dict['object_reference'] = RemoteObjectRef.from_dict(data_dict['object_reference'])

        if 'arguments' in data_dict and data_dict['arguments'] is not None:
            decoded_args = base64.b64decode(data_dict['arguments']).decode('utf-8')
            data_dict['arguments'] = json.loads(decoded_args)

        if 'result' in data_dict and data_dict['result'] is not None:
            decoded_result = base64.b64decode(data_dict['result']).decode('utf-8')
            data_dict['result'] = json.loads(decoded_result)

        msg_type = data_dict.pop('message_type') 
        
        if msg_type == TYPE_REQUEST:
            return RequestMessage(**data_dict)
        elif msg_type == TYPE_REPLY:
            return ReplyMessage(**data_dict)
        raise ValueError("Tipo de mensagem desconhecido")

class RequestMessage(Message):
    def __init__(self, request_id: int, object_reference: RemoteObjectRef, method_id: str, arguments: Dict[str, Any]):
        self.message_type = TYPE_REQUEST
        self.request_id = request_id
        self.object_reference = object_reference
        self.method_id = method_id
        self.arguments = arguments

class ReplyMessage(Message):
    def __init__(self, request_id: int, result: Any = None, exception: str = None):
        self.message_type = TYPE_REPLY
        self.request_id = request_id
        self.result = result
        self.exception = exception