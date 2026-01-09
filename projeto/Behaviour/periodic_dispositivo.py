import jsonpickle
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import random

class PeriodicBehavDispositivo (PeriodicBehaviour):

    async def run(self):
        tipo = self.agent.tipo_dispositivo # "tensiometro", "glicometro", etc.
        valor = None

        # --- LÓGICA DE GERAÇÃO AQUI ---
        # Tens de usar if/elif porque cada aparelho gera dados diferentes
        if tipo == "tensiometro":
            sis = random.randint(110, 150)
            dia = random.randint(70, 95)
            valor = f"{sis}/{dia}"
            
        elif tipo == "glicometro":
            valor = random.randint(70, 140)
            
        elif tipo == "oximetro":
            valor = random.randint(90, 100)

        # --- ENVIO DA MENSAGEM ---
        if valor:
            payload = {
                "tipo_dispositivo": tipo,
                "valor": valor
            }
            
            msg = Message(to=self.agent.jid_destino)
            msg.set_metadata("performative", "inform")
            msg.body = jsonpickle.encode(payload)
            
            await self.send(msg)
            print(f"[{self.agent.name}] Gerou e enviou: {payload}")