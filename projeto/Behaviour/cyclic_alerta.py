import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Classes.perfil_paciente import Perfil_paciente 

class CyclicAlerta(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10) 
        
        if msg:
            try:
                perfil = jsonpickle.decode(msg.body)
                
                if not isinstance(perfil, Perfil_paciente):
                    return

                print(f"[ALERTA] A verificar doenças de: {perfil.nome}")
                
                mensagens_a_enviar = []

                # ======================================================
                # 1. GLICÓMETRO (DIABETES)
                # ======================================================
                if perfil.dados_glicometro is not None:
                    
                    # 1.1 Procura a doença na lista
                    doenca_encontrada = None
                    for d in perfil.doencas:
                        if "diab" in d.lower(): 
                            doenca_encontrada = d
                            break
                    
                    # 1.2 Se encontrou, analisa e prepara mensagem
                    if doenca_encontrada:
                        valor = perfil.dados_glicometro
                        performative = "inform"
                        problema = "Glicemia Controlada"

                        if valor < 50 or valor > 300:
                            performative = "critico"
                            problema = f"Glicemia EXTREMA ({valor})"
                        elif valor > 180 or valor < 70:
                            performative = "urgente"
                            problema = f"Glicemia Descontrolada ({valor})"
                        
                        mensagens_a_enviar.append({
                            "performative": performative,
                            "body": {
                                "tipo_alerta": performative.upper(),
                                "doenca_detetada": doenca_encontrada,
                                "problema": problema,
                                "valor": valor,
                                "perfil_completo": perfil # <--- OBRIGATÓRIO: Envia o perfil
                            }
                        })

                # ======================================================
                # 2. TENSIÓMETRO (HIPERTENSÃO)
                # ======================================================
                if perfil.dados_tensiometro is not None:
                    
                    # 2.1 Procura a doença na lista
                    doenca_encontrada = None
                    for d in perfil.doencas:
                        if "hiper" in d.lower() or "tens" in d.lower():
                            doenca_encontrada = d
                            break
                    
                    # 2.2 Se encontrou, analisa e prepara mensagem
                    if doenca_encontrada:
                        valor = perfil.dados_tensiometro
                        performative = "inform"
                        problema = "Tensão Controlada"

                        try:
                            if isinstance(valor, str) and "/" in valor:
                                sys, dia = map(int, valor.split('/'))
                                
                                if sys > 180 or dia > 110:
                                    performative = "critico"
                                    problema = f"CRISE HIPERTENSIVA ({valor})"
                                elif sys > 140 or dia > 90:
                                    performative = "urgente"
                                    problema = f"Tensão Elevada ({valor})"
                        except:
                            pass

                        mensagens_a_enviar.append({
                            "performative": performative,
                            "body": {
                                "tipo_alerta": performative.upper(),
                                "doenca_detetada": doenca_encontrada,
                                "problema": problema,
                                "valor": valor,
                                "perfil_completo": perfil # <--- OBRIGATÓRIO: Envia o perfil
                            }
                        })

                # ======================================================
                # 3. OXÍMETRO (DPOC)
                # ======================================================
                if perfil.dados_oximetro is not None:
                    
                    # 3.1 Procura a doença na lista
                    doenca_encontrada = None
                    for d in perfil.doencas:
                        if "dpoc" in d.lower():
                            doenca_encontrada = d
                            break
                    
                    # 3.2 Se encontrou, analisa e prepara mensagem
                    if doenca_encontrada:
                        valor = perfil.dados_oximetro
                        performative = "inform"
                        problema = "Saturação O2 Normal"

                        if valor < 85:
                            performative = "critico"
                            problema = f"Hipoxia Severa ({valor}%)"
                        elif valor < 90:
                            performative = "urgente"
                            problema = f"Saturação Baixa ({valor}%)"

                        mensagens_a_enviar.append({
                            "performative": performative,
                            "body": {
                                "tipo_alerta": performative.upper(),
                                "doenca_detetada": doenca_encontrada,
                                "problema": problema,
                                "valor": valor,
                                "perfil_completo": perfil # <--- OBRIGATÓRIO: Envia o perfil
                            }
                        })

                # ======================================================
                # 4. ENVIO DE TODAS AS MENSAGENS GERADAS
                # ======================================================
                plataforma_jid = self.agent.get("plataforma_jid")
                
                if plataforma_jid and mensagens_a_enviar:
                    for item in mensagens_a_enviar:
                        msg_out = Message(to=plataforma_jid)
                        
                        # Define a Performative (inform, urgente, critico)
                        msg_out.set_metadata("performative", item["performative"])
                        
                        # O Body leva tudo (doença + perfil + valor)
                        msg_out.body = jsonpickle.encode(item["body"])
                        
                        await self.send(msg_out)
                        print(f"--> Para Plataforma ({item['performative']}): {item['body']['doenca_detetada']}")

            except Exception as e:
                print(f"Erro: {e}")