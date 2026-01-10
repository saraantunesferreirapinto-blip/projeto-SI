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
<<<<<<< HEAD
        
            dados_paciente = jsonpickle.decode(msg.body)
            id_alerta_recebido = dados_paciente.get("id_alerta") 
            problema = dados_paciente.get("doenca_detetada", "Problema não especificado")
            perfil_paciente = dados_paciente.get("conteudo_completo", {})
=======
            print(f"[{self.agent.jid}] Recebi um pedido de ajuda!")

            dados_paciente = jsonpickle.decode(msg.body)
>>>>>>> 4e85d73f58f2eaf98d9876a8751dbf49e19c3aee
            recomendacao = None

            # Definimos apenas qual é a recomendação com base no nível de urgência
            if performative == "informativo":
                recomendacao = "Recomendação terapêutica: Ajustar medicação"
            
            elif performative == "urgente":
                recomendacao = "Contacto com o paciente necessário"
            
            elif performative == "critico":
                recomendacao = "Pedido de observação presencial imediata"

            if recomendacao:
<<<<<<< HEAD
                print(f"   Dr. Analisou: '{problema}' -> Rx: {recomendacao}")

                payload_resposta = {
                    "id_alerta": id_alerta_recebido, 
                    "acao_recomendada": recomendacao,
                    "medico_responsavel": str(self.agent.jid),
                    "perfil_completo": perfil_paciente 
                }

                msg_resposta = msg.make_reply()
                msg_resposta.set_metadata("performative", "request")
                msg_resposta.body = jsonpickle.encode(payload_resposta)
                
                await self.send(msg_resposta)
                print(f" [{self.agent.name}] Resposta enviada (via Reply).")
            
            elif performative == "agree":
                print("Registo confirmado na plataforma.")

            else:
                print(f"Médico: Não foi gerada recomendação para performative: {performative}")
=======
                # Preparar o dicionário de resposta
                mensagens_a_enviar = {
                    "acao_recomendada": recomendacao,
                    "dados_originais": dados_paciente # Opcional: devolver os dados para contexto
                }

                # 2. Criar 
                msg_plataforma = Message(to=str(msg.sender))
                msg_plataforma.set_metadata("performative", "request") 
                
                # 3. CORREÇÃO CRÍTICA: Codificar o dicionário para String
                msg_plataforma.body = jsonpickle.encode(mensagens_a_enviar)
                
                await self.send(msg_plataforma)
                print(f"[{self.agent.name}] Enviou parecer: '{recomendacao}'")
            
            else:
                print(f"[{self.agent.name}] Recebi performative desconhecido: {performative}")

>>>>>>> 4e85d73f58f2eaf98d9876a8751dbf49e19c3aee
        else:
            pass