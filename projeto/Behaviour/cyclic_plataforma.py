from spade.behaviour import CyclicBehaviour
from spade.message import Message

import asyncio
import jsonpickle
import math
import time

class CyclicBehavPlataforma(CyclicBehaviour):

    async def on_end(self):
        await self.agent.stop()

    def filtrar_medicos(self, especialidade):
        medicos_encontrados = []
        # Acede ao dicionário que está guardado no Agente
        for jid, info in self.agent.medico_subscribe.items():
            if info.get('especialidade', '').lower() == especialidade.lower():
                medicos_encontrados.append(jid)
        return medicos_encontrados    

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
                # jsonpickle reconstrói o objeto Perfil_medico
                perfil_obj = jsonpickle.decode(msg.body) 
                jid_medico = str(msg.sender)

                # Convertemos o objeto para dicionário usando a tua função
                # Isto resolve o erro do .get()
                dados_formatados = perfil_obj.formatar_perfil()

                # Guardamos no dicionário da Plataforma
                self.agent.medico_subscribe[jid_medico] = dados_formatados
                
                print(f"✅ Médico {jid_medico} registado com sucesso!")
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
                # --- 1. Extração de Dados ---
                
                dados_alerta = jsonpickle.decode(msg.body)
                doenca = dados_alerta.get("doenca_detetada", "").lower()
                
                # Removido o self.mapear_especialidade porque o mapeamento está abaixo
                perfil_paciente = dados_alerta.get("conteudo_completo", {})

                # --- 2. Obter Posição do Paciente ---
                pos_p = perfil_paciente.get("posicao", {'x': 0, 'y': 0})
                px = int(pos_p.get('x', 0))
                py = int(pos_p.get('y', 0))

                # --- 2. Mapeamento Correto (O TEU TRADUTOR) ---
                especialidade_procurada = ""
                if doenca == "diabetes":
                    especialidade_procurada = "endocrinologia"  # Nome que o médico usou no registo
                elif doenca == "hipertensao":
                    especialidade_procurada = "cardiologia"
                elif doenca == "dpoc":
                    especialidade_procurada = "pneumologia"

                print(f"🔎 Doença: {doenca} -> Especialidade necessária: {especialidade_procurada}")

                # --- 3. Filtrar Médicos ---
                # Agora usamos a variável certa que criámos acima
                medicos_disponiveis = self.filtrar_medicos(especialidade_procurada)
                print(f"DEBUG: Encontrei {len(medicos_disponiveis)} médicos para {especialidade_procurada}")

                dist_min = 1000
                jid_destino = None

                # CORREÇÃO AQUI: Itera sobre a lista FILTRADA
                for m_jid in medicos_disponiveis:
                    # Vai buscar os detalhes do médico ao dicionário usando o JID
                    m = self.agent.medico_subscribe.get(m_jid)
                    
                    if m:
                        # Extração segura de dados do dicionário
                        m_disp = m.get('disponibilidade', True)
                        m_pos = m.get('posicao')

                        if m_disp and m_pos:
                            mx, my = int(m_pos['x']), int(m_pos['y'])
                            d = math.sqrt((mx - px)**2 + (my - py)**2)
                            
                            if d < dist_min:
                                dist_min = d
                                medico_atendimento = m_jid # Guardamos o JID para enviar a msg
                                jid_destino = m_jid

                # --- 6. Enviar para o Médico ---
                if jid_destino:
                    print(f"[Plataforma] ✅ A enviar para {jid_destino}")
                    msg_medico = Message(to=jid_destino)
                    msg_medico.set_metadata("performative", performative)
                    msg_medico.body = jsonpickle.encode(perfil_paciente)
                    await self.send(msg_medico)

            elif performative == "request":
                try:
                    # 1. Descodificar a resposta do médico
                    resposta_medico = jsonpickle.decode(msg.body)
                    recomendacao = resposta_medico.get("acao_recomendada")
                    dados_originais = resposta_medico.get("dados_originais")
                    
                    # 2. Obter o JID do paciente que gerou o alerta
                    # Assumindo que o médico devolveu os 'dados_originais' que enviámos
                    jid_paciente = dados_originais.get("jid")

                    if jid_paciente:
                        print(f"[Plataforma] 📨 Reencaminhando recomendação do {msg.sender} para o paciente {jid_paciente}")
                        
                        # 3. Criar a mensagem para o paciente
                        msg_para_paciente = Message(to=jid_paciente)
                        msg_para_paciente.set_metadata("performative", "inform")
                        msg_para_paciente.body = jsonpickle.encode({
                            "medico": str(msg.sender),
                            "recomendacao": recomendacao
                        })
                        
                        await self.send(msg_para_paciente)
                    else:
                        print(f"[Plataforma] ❌ Erro: Não foi possível identificar o paciente na resposta do médico.")

                except Exception as e:
                    print(f"[Plataforma] Erro ao processar resposta do médico: {e}")        