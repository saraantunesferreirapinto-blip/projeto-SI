from spade.behaviour import CyclicBehaviour
from spade.message import Message

import asyncio
import jsonpickle

class CyclicBehavAlerta(CyclicBehaviour):
    async def on_start(self):
        print("CyclicBehavAlerta starting ...")

    async def run(self):
        msg = await self.receive(timeout = 10)

        if msg:
            p = msg.get_metadata("performative")

            if p == "inform":
                valores_dic = jsonpickle.decode(msg.body)
                tensao = valores_dic["tensiometro"]
                glicemia = valores_dic["glicometro"]
                oxigenio = valores_dic["oximetro"]

                valores_tensao = tensao.split("/")
                sistolica = valores_tensao[0]
                diastolica = valores_tensao[1]

                if sistolica > 90 and sistolica < 120 and diastolica > 60 and diastolica < 84:
                    msg_to_manager = Message(to=self.jid_medico)  
                    msg_to_manager.body = "Alerta informativo"  
                    msg_to_manager.set_metadata("performative", "inform")

                elif sistolica > 130 and sistolica < 159 and sistolica > 80 and sistolica < 89 and diastolica > 85 and diastolica < 99 and diastolica > 50 and diastolica < 59:
                    msg_to_manager = Message(to=self.jid_medico)  
                    msg_to_manager.body = "Alerta urgente"  
                    msg_to_manager.set_metadata("performative", "urgente")

                elif sistolica > 160 and sistolica < 80 and diastolica > 100 and diastolica < 50:
                    msg_to_manager = Message(to=self.jid_medico)  
                    msg_to_manager.body = "Alerta crítico"  
                    msg_to_manager.set_metadata("performative", "critico")

            elif p == "failure":


            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")
