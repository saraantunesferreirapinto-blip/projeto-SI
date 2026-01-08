import random
from projeto.Classes.dispositivo import Dispositivo

class Tensiometro(Dispositivo):
    tipo = "tensiometro"

    def gerar_dados(self):
        return {
            "tipo": self.tipo,
            "sistolica": random.randint(110, 140),
            "diastolica": random.randint(70, 90),
            "unidade": "mmHg"
        }
