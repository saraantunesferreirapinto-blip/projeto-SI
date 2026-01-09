import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import random

class PeriodicBehavDispositivo (PeriodicBehaviour):

    async def run(self):
        tipo = self.agent.tipo_dispositivo 
        valor = None

        if random.random() < 0.2: 
            # SIMULAÇÃO DE ERRO
            payload = {
                "tipo_dispositivo": tipo,
                "valor": None,       
            }
            print(f"[{self.agent.name}] Simulei uma falha!")

            msg = Message(to=self.agent.jid_paciente)
            msg.set_metadata("performative", "failure")
            msg.body = jsonpickle.encode(payload)

            await self.send(msg)

        else:
            if tipo == "tensiometro":
                sis = random.randint(110, 150)
                dia = random.randint(70, 95)
                valor = f"{sis}/{dia}"
                
            elif tipo == "glicometro":
                valor = random.randint(70, 140)
                
            elif tipo == "oximetro":
                valor = random.randint(90, 100)

            if valor:
                payload = {
                    "tipo_dispositivo": tipo,
                    "valor": valor
                }
                
                msg = Message(to=self.agent.jid_paciente)
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(payload)
            
                await self.send(msg)
                print(f"[{self.agent.name}] Gerou e enviou: {payload}")