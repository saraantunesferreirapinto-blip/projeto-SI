import random
from projeto.Classes.dispositivo import Dispositivo

class Oximetro(Dispositivo):
    tipo = "oximetro"

    def gerar_dados(self):
        return {
            "tipo": self.tipo,
            "valor": random.randint(0, 100),
            "unidade": "%"
        }
