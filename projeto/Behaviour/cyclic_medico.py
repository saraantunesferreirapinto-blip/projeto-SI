import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

class CyclicBehavMedico(CyclicBehaviour):

    async def run(self):
        print(f"[{self.agent.name}] Médico à espera de pedidos...")
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
        
            dados_paciente = jsonpickle.decode(msg.body)
            recomendacao = None

            # Definimos apenas qual é a recomendação com base no nível de urgência
            if performative == "informativo":
                recomendacao = "Recomendação terapêutica: Ajustar medicação"
            
            elif performative == "urgente":
                recomendacao = "Contacto com o paciente necessário"
            
            elif performative == "critico":
                recomendacao = "Pedido de observação presencial imediata"

            if recomendacao:
                # Preparar o dicionário de resposta
                mensagens_a_enviar = {
                    "acao_recomendada": recomendacao,
                    "dados_originais": dados_paciente # Opcional: devolver os dados para contexto
                }

                # 2. Criar mensagem
                msg_plataforma = Message(to=self.agent.jid_plataforma)
                msg_plataforma.set_metadata("performative", "request") 
                
                # 3. CORREÇÃO CRÍTICA: Codificar o dicionário para String
                msg_plataforma.body = jsonpickle.encode(mensagens_a_enviar)
                
                await self.send(msg_plataforma)
                print(f"[{self.agent.name}] Enviou parecer: '{recomendacao}'")
            
            else:
                print(f"[{self.agent.name}] Recebi performative desconhecido: {performative}")

        else:
            pass