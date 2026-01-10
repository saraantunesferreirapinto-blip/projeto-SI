import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Classes.perfil_paciente import Perfil_paciente 

class CyclicBehavAlerta(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 

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
                    
                    if isinstance(valor_glic, int):
                        if valor_glic < 50 or valor_glic > 300:
                            performative = "critico"
                            problema = f"Glicemia EXTREMA ({valor_glic})"
                        elif valor_glic > 180 or valor_glic < 70:
                            performative = "urgente"
                            problema = f"Glicemia Descontrolada ({valor_glic})"
                    
                    
                    mensagens_a_enviar.append({
                        "performative": performative,
                        "body": {
                            "tipo_alerta": performative.upper(),
                            "doenca_detetada": "diabetes",
                            "problema": problema,
                            "valor": valor_glic,
                            "conteudo_completo": conteudo 
                        }
                    })

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

                    mensagens_a_enviar.append({
                        "performative": performative,
                        "body": {
                            "tipo_alerta": performative.upper(),
                            "doenca_detetada": "hipertensao",
                            "problema": problema,
                            "valor": valor_tens,
                            "conteudo_completo": conteudo 
                        }
                    })

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

                    mensagens_a_enviar.append({
                        "performative": performative,
                        "body": {
                            "tipo_alerta": performative.upper(),
                            "doenca_detetada": "dpoc",
                            "problema": problema,
                            "valor": valor_oxi,
                            "conteudo_completo": conteudo
                        }
                    })
                # ENVIO DE TODAS AS MENSAGENS GERADAS
                destino = self.agent.get("plataforma_jid")

                
                if destino and mensagens_a_enviar:
                    for item in mensagens_a_enviar:
                        msg_out = Message(to=destino)
                        
                        # Define a Performative (inform, urgente, critico)
                        msg_out.set_metadata("performative", item["performative"])
                        
                        # O Body leva tudo (doença + conteudo + valor)
                        msg_out.body = jsonpickle.encode(item["body"])
                        
                        await self.send(msg_out)
                        print(f"--> Para Médico ({item['performative']}): {item['body']['doenca_detetada']}")

            elif performative == "failure":
                perfil = jsonpickle.decode(msg.body)
                
                if not isinstance(perfil, Perfil_paciente):
                    return

                print(f"[ALERTA] A verificar doenças de: {perfil.nome}")
                
                mensagens_a_enviar = []

                # GLICÓMETRO (DIABETES)
                tem_diabetes = any("diab" in d.lower() for d in perfil.doencas)
                        
                if tem_diabetes:
                    # Se tem diabetes e recebemos failure, o sensor falhou
                    performative = "critico"
                    problema = "Falha na leitura do Glicómetro"
                    valor = "N/A" # Não há valor numa falha
                    
                    mensagens_a_enviar.append({
                        "performative": performative,
                        "body": {
                            "tipo_alerta": performative.upper(),
                            "doenca_detetada": "diabetes",
                            "problema": problema,
                            "valor": valor,
                            "conteudo_completo": perfil # Enviamos o perfil para contexto
                        }
                    })

                # TENSIÓMETRO (HIPERTENSÃO)
                tem_hipertensao = any(("hiper" in d.lower() or "tens" in d.lower()) for d in perfil.doencas)
                        
                if tem_hipertensao:
                    performative = "critico"
                    problema = "Falha na leitura do Tensiometro"
                    valor = "N/A"

                    mensagens_a_enviar.append({
                        "performative": performative,
                        "body": {
                            "tipo_alerta": performative.upper(),
                            "doenca_detetada": "hipertensao",
                            "problema": problema,
                            "valor": valor,
                            "conteudo_completo": perfil
                        }
                    })

                # OXÍMETRO (DPOC)
                tem_dpoc = any("dpoc" in d.lower() for d in perfil.doencas)
                        
                if tem_dpoc:
                    performative = "critico"
                    problema = "Falha na leitura do Oximtro"
                    valor = "N/A"

                    mensagens_a_enviar.append({
                        "performative": performative,
                        "body": {
                            "tipo_alerta": performative.upper(),
                            "doenca_detetada": "dpoc",
                            "problema": problema,
                            "valor": valor,
                            "conteudo_completo": perfil
                        }
                    })

                # MUDANÇA: ENVIO SEMPRE PARA A PLATAFORMA
                destino = self.agent.get("plataforma_jid")
                
                if destino and mensagens_a_enviar:
                    for item in mensagens_a_enviar:
                        msg_out = Message(to=destino)
                        
                        # Mantemos a performative (critico/urgente) para a plataforma saber a prioridade
                        msg_out.set_metadata("performative", item["performative"])
                                                
                        msg_out.body = jsonpickle.encode(item["body"])
                        
                        await self.send(msg_out)
                        print(f"[{self.agent.name}] Encaminhado para a PLATAFORMA: {item['body']['problema']}")

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")
                
        else:
            print("Paciente: Nenhuma mensagem recebida recentemente.")