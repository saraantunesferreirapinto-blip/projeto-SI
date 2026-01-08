import random
from projeto.Classes.dispositivo import Dispositivo

class Glicometro(Dispositivo):
    tipo = "glicometro"

    def gerar_dados(self):
        return {
            "tipo": self.tipo,
            "valor": random.randint(70, 180),
            "unidade": "mg/dL"
        }
