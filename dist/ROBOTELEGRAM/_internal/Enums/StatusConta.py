from enum import Enum

class StatusConta(Enum):
    CONECTADA = 0
    NAO_AUTENTICADA = 1
    FALHA = 2
    FLOOD = 3
    TAREFA = 4