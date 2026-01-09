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


                if (sistolica >= 160 or sistolica < 80 or diastolica >= 100 or diastolica < 50 or
                    oxigenio < 90 or glicemia < 60 or glicemia > 250):
                    msg_to_manager = Message(to=self.jid_medico)  
                    msg_to_manager.body = "Alerta informativo"  
                    msg_to_manager.set_metadata("performative", "informativo")

                elif (
                    130 <= sistolica <= 159 or 80 <= sistolica <= 89 or
                    85 <= diastolica <= 99 or 50 <= diastolica <= 59 or
                    90 <= oxigenio <= 94 or
                    60 <= glicemia <= 69 or 141 <= glicemia <= 250):
                    msg_to_manager = Message(to=self.jid_medico)  
                    msg_to_manager.body = "Alerta urgente"  
                    msg_to_manager.set_metadata("performative", "urgente")

                else: 
                    msg_to_manager = Message(to=self.jid_medico)  
                    msg_to_manager.body = "Alerta informativo"  
                    msg_to_manager.set_metadata("performative", "informativo")

            elif p == "failure":


            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 10 seconds")
