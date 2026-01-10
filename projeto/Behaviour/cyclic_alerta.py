import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Classes.alerta import Alerta
import time

class CyclicBehavAlerta(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=5) 

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "inform":
                conteudo = jsonpickle.decode(msg.body)

                if isinstance(conteudo, dict) and "paciente" in conteudo:
                    nome = conteudo.get("paciente")
                    sinais = conteudo.get("sinais_vitais", {})
                    
                    print(f"[{self.agent.name}] 🔎 A analisar vitais de: {nome}")
                    
                    mensagens_a_enviar = []

                # 1. GLICÓMETRO (DIABETES)
                valor_glic = sinais.get("glicometro")
                if valor_glic is not None:
                    problema = "Glicemia Estável"
                    performative = "informativo"
                    if valor_glic < 50 or valor_glic > 300:
                        performative = "critico"
                        problema = f"Glicemia EXTREMA ({valor_glic})"
                    elif valor_glic > 180 or valor_glic < 70:
                        performative = "urgente"
                        problema = f"Glicemia Descontrolada ({valor_glic})"
                    
                    novo_alerta = Alerta(
                                agente_nome=self.agent.name,
                                performative=performative,
                                doenca="diabetes",
                                problema=problema,
                                valor=valor_glic,
                                conteudo=conteudo
                            )
                    mensagens_a_enviar.append(novo_alerta)

                # 2. TENSIÓMETRO (HIPERTENSÃO)
                valor_tens = sinais.get("tensiometro")
                if valor_tens is not None:
                    problema = "Tensão Normal"
                    performative = "informativo"

                    try:
                        if isinstance(valor_tens, str) and "/" in valor_tens:
                            sys, dia = map(int, valor_tens.split('/'))
                            if sys > 180 or dia > 110:
                                performative = "critico"
                                problema = f"CRISE HIPERTENSIVA ({valor_tens})"
                            elif sys > 140 or dia > 90:
                                performative = "urgente"
                                problema = f"Tensão Elevada ({valor_tens})"
                    except:
                        pass

                    novo_alerta = Alerta(
                                agente_nome=self.agent.name,
                                performative=performative,
                                doenca="hipertensao",
                                problema=problema,
                                valor=valor_tens,
                                conteudo=conteudo
                            )
                    mensagens_a_enviar.append(novo_alerta)

                # OXÍMETRO (DPOC)
                valor_oxi = sinais.get("oximetro")
                if valor_oxi is not None:
                    problema = "Saturação OK"
                    performative = "informativo"
                    
                    if isinstance(valor_oxi, int):
                        if valor_oxi < 85:
                            performative = "critico"
                            problema = f"Hipoxia Severa ({valor_oxi}%)"
                        elif valor_oxi < 90:
                            performative = "urgente"
                            problema = f"Saturação Baixa ({valor_oxi}%)"

                    novo_alerta = Alerta(
                                agente_nome=self.agent.name,
                                performative=performative,
                                doenca="dpoc",
                                problema=problema,
                                valor=valor_oxi,
                                conteudo=conteudo
                            )
                    mensagens_a_enviar.append(novo_alerta)

                # ENVIO DE TODAS AS MENSAGENS GERADAS
                destino = self.agent.get("plataforma_jid")

                if destino and mensagens_a_enviar:
                    for item in mensagens_a_enviar:
                        msg_out = Message(to=destino)
                        
                        # Define a Performative (inform, urgente, critico)
                        msg_out.set_metadata("performative", item._performative_envio)
                        
                        # O Body leva tudo (doença + conteudo + valor)
                        msg_out.body = jsonpickle.encode(item.dict())
                        
                        await self.send(msg_out)
                        print(f"--> Para Médico ({item._performative_envio}): {item.doenca_detetada}")

            elif performative == "failure":
                perfil = jsonpickle.decode(msg.body)
                
                mensagens_a_enviar = []

                # GLICÓMETRO (DIABETES)
                if any("diab" in d.lower() for d in perfil.doencas):
                    # Cria o objeto Alerta diretamente
                    # Nota: Valor é "N/A" e performative é sempre "critico"
                    novo_alerta = Alerta(
                        agente_nome=self.agent.name,
                        performative="critico",
                        doenca="diabetes",
                        problema="Falha na leitura do Glicómetro",
                        valor="N/A",
                        conteudo=perfil
                    )
                    mensagens_a_enviar.append(novo_alerta)

                # TENSIÓMETRO (HIPERTENSÃO)
                if any(("hiper" in d.lower() or "tens" in d.lower()) for d in perfil.doencas):
                    novo_alerta = Alerta(
                        agente_nome=self.agent.name,
                        performative="critico",
                        doenca="hipertensao",
                        problema="Falha na leitura do Tensiómetro",
                        valor="N/A",
                        conteudo=perfil
                    )
                    mensagens_a_enviar.append(novo_alerta)

                # OXÍMETRO (DPOC)
                if any("dpoc" in d.lower() for d in perfil.doencas):
                    novo_alerta = Alerta(
                        agente_nome=self.agent.name,
                        performative="critico",
                        doenca="dpoc",
                        problema="Falha na leitura do Oxímetro",
                        valor="N/A",
                        conteudo=perfil
                    )
                    mensagens_a_enviar.append(novo_alerta)

                # MUDANÇA: ENVIO SEMPRE PARA A PLATAFORMA
                destino = self.agent.get("plataforma_jid")
                
                if destino and mensagens_a_enviar:
                    for item in mensagens_a_enviar:
                        msg_out = Message(to=destino)
                        
                        # Mantemos a performative (critico/urgente) para a plataforma saber a prioridade
                        msg_out.set_metadata("performative", item._performative_envio)
                        msg_out.body = jsonpickle.encode(item.dict())
                        
                        await self.send(msg_out)
                        print(f"[{self.agent.name}] Encaminhado para a PLATAFORMA: {item.problema}")

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")
                
        else:
            print("Paciente: Nenhuma mensagem recebida recentemente.")