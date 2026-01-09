from spade.behaviour import CyclicBehaviour
from spade.message import Message

import asyncio
import jsonpickle
import math
import time

class CyclicBehavPlataforma(CyclicBehaviour):

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
            #FAILURE
            ####################################################################
            elif performative == "failure":
                # O remetente da mensagem (quem falhou, ex: o dispositivo ou paciente)
                remetente = str(msg.sender)

                if not hasattr(self.agent, "historico_falhas"):
                    self.agent.historico_falhas = {}

                if remetente not in self.agent.historico_falhas:
                    self.agent.historico_falhas[remetente] = []

                import time # Podes importar no topo do ficheiro também
                agora = time.time()
                self.agent.historico_falhas[remetente].append(agora)
 
                num_falhas = len(self.agent.historico_falhas[remetente])
                
                print(f"PLATAFORMA: Registada falha de {remetente}. Total de falhas recentes: {num_falhas}")
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
            
                especialidade=""
                if doenca=="diabetes":
                    especialidade="diabetes"
                elif doenca=="hipertensão":
                    especialidade="coração"
                elif doenca=="hipóxia":
                    especialidade="oxigénio"
                
                medicos_especialidade=[]
                for m in self.agent.medico_subscribe:
                    if m.especialidade==especialidade and m.disponibilidade==True:
                        medicos_especialidade.append(m)
                
                medico_atendimento=None
                dist_min=1000

                for medico in medicos_especialidade:
                    d=math.srqt(
                        math.pow(medico.getPosition().getX()-perfil_paciente.getPosition().getX(),2)+
                        math.pow(medico.getPosition().getY()-perfil_paciente.getPosition().getY(),2)
                    )
                    if d<dist_min:
                        dist_min=d
                        medico_escolhido = medico
                
                if medico_atendimento:
                    destinatario_jid=str(medico_escolhido.getAgent())
                    msg_para_medico=Message(to=destinatario_jid)
                    msg_para_medico.set_metadata("performative",performative)
                    msg_para_medico.body=jsonpickle.encode(dados_alerta)
                    await self.send(msg_para_medico)

                print(f"--- SUCESSO ---")
                print(f"Alerta {performative.upper()} enviado para o especialista: {destinatario_jid}")
                

 