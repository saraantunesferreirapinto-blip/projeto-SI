from spade.behaviour import CyclicBehaviour
from spade.message import Message

import asyncio
import jsonpickle

class cyclic_plataforma(CyclicBehaviour):

    async def on_end(self):
        await self.agent.stop()

    async def run(self):
        msg = await self.receive(timeout=10)  # wait for a message for 10 seconds

        if msg:

            performative = msg.get_metadata("performative")
            ####################################################################
            #EXISTENCIA DO PACIENTE
            ####################################################################
            if performative == "subscribe":  # verificar nome da performative ###########################################################################################333
                paciente_info = jsonpickle.decode(msg.body)
                self.agent.paciente_subscribe.append(paciente_info)######criar no agente
                print("Agent {}:".format(str(self.agent.jid)) + " Paciente Agent {} registered!".format(str(msg.sender)))################################sender
                #print(f"Plataforma {self.agent.jid}: Paciente {msg.sender} registado com sucesso!")
            ####################################################################
            #EXISTENCIA DO MEDICO
            ####################################################################           
            elif performative == "propose":  # verificar nome da performative ###########################################################################################333
                medico_info = jsonpickle.decode(msg.body)
                self.agent.medico_subscribe.append(medico_info)##############criar no agente
                print("Agent {}:".format(str(self.agent.jid)) + " Medico Agent {} registered!".format(str(msg.sender)))################################sender
                #print(f"Plataforma {self.agent.jid}: Médico {msg.sender} disponível no sistema!")
            ####################################################################
            #ENVIO PARA O MEDICO
            ####################################################################
            elif performative in["urgente","critico","informativo"]:#verificar o nome da performative ############################################################################################################33
                print(f"Plataforma: Alerta {performative.upper()} recebido de {msg.sender}")
                dados_alerta=jsonpickle.decode(msg.body)
                #dados necessários
                doenca = dados_alerta["doenca_detetada"]
                perfil_paciente= dados_alerta["perfil_completo"]
                print(f"ALERTA {performative.upper()} recebido: {doenca} para o paciente {perfil_paciente.jid}")
            
                


 