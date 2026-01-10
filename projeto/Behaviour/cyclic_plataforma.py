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
                
                # --- 1. Extração de Dados ---
                doenca = dados_alerta["doenca_detetada"]
                perfil_paciente= dados_alerta["conteudo_completo"]
                jid_paciente = perfil_paciente.get("jid", "Desconhecido")
                print(f"ALERTA {performative.upper()} recebido: {doenca} para o paciente {jid_paciente}")

                # --- 2. Mapeamento da Especialidade ---
                especialidade=""
                if doenca=="diabetes":
                    especialidade="diabetes"
                elif doenca=="hipertensão":
                    especialidade="coração"
                elif doenca=="hipóxia":
                    especialidade="oxigénio"
                
                # --- 3. Filtrar Médicos Disponíveis ---
                medicos_especialidade=[]
                for m in self.agent.medico_subscribe:
                    if m.especialidade==especialidade and m.disponibilidade==True:
                        medicos_especialidade.append(m)

                # --- 4. Calcular Distância (Euclidiana) ---
                medico_atendimento=None
                dist_min=1000
                # Posição do PACIENTE (Vem do JSON como dicionário)
                pos_paciente = perfil_paciente.get("posicao", {'x': 0, 'y': 0})
                px = int(pos_paciente.get('x', 0))
                py = int(pos_paciente.get('y', 0))

                for medico in medicos_especialidade:
                    if medico.posicao: # Verifica se o médico tem posição definida
                        mx = medico.posicao.x
                        my = medico.posicao.y
                        
                        d = math.sqrt(math.pow(mx - px, 2) + math.pow(my - py, 2))
                        
                        print(f"   -> Médico {medico.nome} ({medico.jid_medico}) está a {d:.2f}m")

                        if d < dist_min:
                            dist_min = d
                            medico_atendimento = medico
                    else:
                        print(f"   -> Médico {medico.nome} ignorado (sem posição definida).")        

                # --- 5. Enviar Mensagem ---
                if medico_atendimento:
                    # Usamos o atributo jid_medico da tua classe
                    destinatario_jid = str(medico_atendimento.jid_medico)
                    
                    msg_para_medico = Message(to=destinatario_jid)
                    msg_para_medico.set_metadata("performative", performative)
                    msg_para_medico.body = jsonpickle.encode(dados_alerta)
                    
                    await self.send(msg_para_medico)

                    print(f"--- SUCESSO ---")
                    print(f"Alerta enviado para: {medico_atendimento.nome} (Dist: {dist_min:.1f})")        