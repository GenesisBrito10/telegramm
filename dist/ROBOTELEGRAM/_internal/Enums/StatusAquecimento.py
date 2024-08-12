from enum import Enum

class StatusAquecimento(Enum):
    AQUECENDO = 1
    FALHA = 2
    REMOVENDO_AQUECIMENTO = 3
    FINALIZADO = 4