import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.message import Message
from Classes.position import Position

import jsonpickle
import math


class cyclic_paciente(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            dado = jsonpickle.decode(msg.body)
            tipo = type(dado).__name__
            
            # Aceder ao perfil guardado no agente
            perfil = self.agent.perfil 

            if tipo == "Tensiometro":
                perfil.dados_tensiometro = f"{dado['sistolica']}/{dado['diastolica']}"
            elif tipo == "Oximetro":
                perfil.dados_oximetro = dado['valor']
            elif tipo == "Glicometro":
                perfil.dados_glicometro = dado['valor']

        else:
                # Medida de contingência: alerta de falha de comunicação 
                print(f"[{self.agent.name}] erro: timeout na receção de dados!") 