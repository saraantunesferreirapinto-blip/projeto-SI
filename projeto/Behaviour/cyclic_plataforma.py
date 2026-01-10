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
        remetente = str(msg.sender)

        if msg:
            performative = msg.get_metadata("performative")
            ####################################################################
            #EXISTENCIA DO PACIENTE
            ####################################################################
            if performative == "subscribe":  # verificar nome da performative ###########################################################################################333
                paciente_info = jsonpickle.decode(msg.body)
                self.agent.paciente_subscribe.append(paciente_info)######criar no agente
                print("Agent {}:".format(str(self.agent.jid)) + " Paciente Agent {} registered!".format(remetente))################################
                
                reply = msg.make_reply()
                reply.set_metadata("performative", "agree") # 'agree' confirma a subscrição
                reply.body = "Registo efetuado com sucesso na Plataforma."
                await self.send(reply)
            ####################################################################
            #EXISTENCIA DO MEDICO
            ####################################################################           
            elif performative == "propose":  # verificar nome da performative ###########################################################################################333
                # jsonpickle reconstrói o objeto Perfil_medico
                perfil_obj = jsonpickle.decode(msg.body) 

                # Convertemos o objeto para dicionário usando a tua função
                # Isto resolve o erro do .get()
                dados_formatados = perfil_obj.formatar_perfil()

                # Guardamos no dicionário da Plataforma
                self.agent.medico_subscribe[remetente] = dados_formatados
                
                print(f"✅ Médico {remetente} registado com sucesso!")
                reply = msg.make_reply()
                reply.set_metadata("performative", "agree")
                reply.body = "Registo de médico aceite."
                await self.send(reply)

            ####################################################################
            #FAILURE
            ####################################################################
            elif performative == "failure":
                try:
                    conteudo_falha = jsonpickle.decode(msg.body)
                except:
                    conteudo_falha = {"erro": "Conteúdo ilegível", "jid": remetente}

                if remetente not in self.agent.historico_falhas:
                    self.agent.historico_falhas[remetente] = []

                # Em vez de guardar só o tempo, guardamos um objeto completo
                registo = {
                    "timestamp": time.time(),
                    "conteudo": conteudo_falha  # Aqui fica o perfil/dados
                }

                self.agent.historico_falhas[remetente].append(registo)
                
                print(f"PLATAFORMA: Falha registada de {remetente} com dados anexados.")
            ####################################################################
            #ENVIO PARA O MEDICO
            ####################################################################
            elif performative in["urgente","critico","informativo"]:#verificar o nome da performative ############################################################################################################33
                # --- 1. Extração de Dados ---
                dados_dict = jsonpickle.decode(msg.body)
                doenca = dados_dict.get("doenca_detetada", "").lower()
                
                # Removido o self.mapear_especialidade porque o mapeamento está abaixo
                perfil_paciente = dados_dict.get("conteudo_completo", {})

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

                medico_final = None
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
                                medico_final = m_jid # Guardamos o JID para enviar a msg   

                id_alerta = dados_dict.get("id_alerta")
                # --- 5. Enviar Mensagem ---
                if medico_final:
                    destinatario_jid = str(medico_final.jid_medico)

                    self.agent.alertas_pendentes[id_alerta] = {
                        "medico_atual": destinatario_jid,
                        "conteudo": dados_dict,
                        "performative_orig": performative, # <--- IMPORTANTE PARA O PERIODIC SABER O TIPO
                        "tentativas": 1,
                        "ultima_tentativa": time.time(),
                        "status": "pendente"
                    }
                    
                    msg_para_medico = Message(to=destinatario_jid)
                    msg_para_medico.set_metadata("performative", performative)
                    msg_para_medico.body = jsonpickle.encode(dados_dict)
                    
                    await self.send(msg_para_medico)

                    print(f"--- SUCESSO ---")
                    print(f"Alerta enviado para: {medico_final.nome} (Dist: {dist_min:.1f})")  

            elif performative == "request":  
    
                try:
                    # A. Descodificar
                    resposta_medico = jsonpickle.decode(msg.body)
                    # Proteção extra caso venha string
                    if isinstance(resposta_medico, str):
                        resposta_medico = jsonpickle.decode(resposta_medico)

                    # B. Fechar Pendente
                    if "id_alerta" in resposta_medico:
                        id_res = resposta_medico["id_alerta"]
                        if id_res in self.agent.alertas_pendentes:
                            self.agent.alertas_pendentes[id_res]["status"] = "resolvido"
                            print(f"Plataforma: Caso {id_res} resolvido.")

                    # C. Encaminhar para Paciente
                    # O médico devolve o 'perfil_completo' que nós lhe enviámos. O JID está lá.
                    perfil_p = resposta_medico.get("perfil_completo", {})
                    # Fallback: tentar dados_originais se perfil_completo falhar
                    if not perfil_p:
                        perfil_p = resposta_medico.get("dados_originais", {}).get("conteudo_completo", {})

                    jid_paciente = perfil_p.get("jid")

                    if jid_paciente:
                        msg_paciente = Message(to=jid_paciente)
                        msg_paciente.set_metadata("performative", "inform")
                        
                        # Limpar dados redundantes antes de enviar ao paciente (opcional)
                        corpo_final = {
                            "medico": remetente,
                            "recomendacao": resposta_medico.get("acao_recomendada"),
                            "id_alerta": resposta_medico.get("id_alerta")
                        }
                        msg_paciente.body = jsonpickle.encode(corpo_final)
                        
                        await self.send(msg_paciente)
                        print(f"✅ Resposta entregue ao paciente {jid_paciente}")
                    else:
                        print(f"❌ ERRO: JID do paciente não encontrado na resposta do médico.")

                except Exception as e:
                    print(f"ERRO ao processar resposta do médico: {e}")