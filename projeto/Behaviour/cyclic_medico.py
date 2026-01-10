import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import json

class CyclicBehavMedico(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            if performative == "agree":
                print(f"[{self.agent.name}] ✅ Confirmação recebida: {msg.body}")
                return

        
            dados_paciente = jsonpickle.decode(msg.body)

            id_alerta_recebido = dados_paciente.get("id_alerta") 
            problema = dados_paciente.get("doenca_detetada", "Problema não especificado")
            perfil_paciente = dados_paciente.get("conteudo_completo", {})

            recomendacao = None

            # Definimos apenas qual é a recomendação com base no nível de urgência
            if performative == "informativo":
                recomendacao = "Recomendação terapêutica: Ajustar medicação"
            

            try:
                # 1. Primeira tentativa de descodificar
                dados_recebidos = jsonpickle.decode(msg.body)
                if recomendacao:
                    # Preparar o dicionário de resposta
                    mensagens_a_enviar = {
                        "acao_recomendada": recomendacao,
                        "dados_originais": dados_paciente # Opcional: devolver os dados para contexto
                    }

                    # 2. Criar mensagem
                    msg_plataforma = Message(to=self.agent.jid_plataforma)

                    # --- DAQUI PARA BAIXO O CÓDIGO É IGUAL ---
                    id_alerta_recebido = dados_recebidos.get("id_alerta") 
                    problema = dados_recebidos.get("doenca_detetada", "Desconhecida")
                    
                    # Tentar obter o perfil
                    perfil_paciente = dados_recebidos.get("conteudo_completo")
                    if not perfil_paciente:
                        perfil_paciente = dados_recebidos.get("perfil_completo", {})

                    recomendacao = None

                    # 2. Criar 
                    msg_plataforma = Message(to=str(msg.sender))

                    msg_plataforma.set_metadata("performative", "request") 
                    
                    # 3. CORREÇÃO CRÍTICA: Codificar o dicionário para String
                    msg_plataforma.body = jsonpickle.encode(mensagens_a_enviar)
                    
                    await self.send(msg_plataforma)
                    print(f"[{self.agent.name}] Enviou parecer: '{recomendacao}'")

                    # Enviar Resposta
                    if recomendacao:
                        print(f"   Dr. Analisou: '{problema}' -> Rx: {recomendacao}")

                        payload_resposta = {
                            "id_alerta": id_alerta_recebido, 
                            "acao_recomendada": recomendacao,
                            "medico_responsavel": str(self.agent.jid),
                            "dados_originais": dados_recebidos,
                            "perfil_completo": perfil_paciente 
                        }

                        msg_resposta = msg.make_reply()
                        msg_resposta.set_metadata("performative", "request")
                        msg_resposta.body = jsonpickle.encode(payload_resposta)
                        
                        await self.send(msg_resposta)
                        print(f" [{self.agent.name}] Parecer enviado.")

            except Exception as e:
                print(f"❌ ERRO ao processar mensagem JSON: {e}")
                print(f"   Conteúdo que causou erro: {msg.body}")