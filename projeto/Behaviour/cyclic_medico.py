import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import json

class CyclicBehavMedico(CyclicBehaviour):

    async def run(self):
        print(f"[{self.agent.name}] Médico à espera de pedidos...")
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "agree":
                print(f"[{self.agent.name}] ✅ Confirmação recebida: {msg.body}")
                return
            

            try:
                # 1. Primeira tentativa de descodificar
                dados_recebidos = jsonpickle.decode(msg.body)

                # --- DAQUI PARA BAIXO O CÓDIGO É IGUAL ---
                id_alerta_recebido = dados_recebidos.get("id_alerta") 
                problema = dados_recebidos.get("doenca_detetada", "Desconhecida")
                
                # Tentar obter o perfil
                perfil_paciente = dados_recebidos.get("conteudo_completo")
                if not perfil_paciente:
                    perfil_paciente = dados_recebidos.get("perfil_completo", {})

                recomendacao = None

                # Lógica de Decisão
                if performative == "informativo":
                    recomendacao = "Recomendação: Monitorizar e hidratar."
                elif performative == "urgente":
                    recomendacao = "Recomendação: Ajustar medicação imediatamente."
                elif performative == "critico":
                    recomendacao = "ALERTA: Encaminhar para urgência hospitalar."

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