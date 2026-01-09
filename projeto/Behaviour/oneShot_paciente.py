import random
import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Classes.position import Position
from Classes.perfil_paciente import Perfil_paciente

class OneShotBehavPaciente(OneShotBehaviour):
    async def run(self):
        # Gerar Posição Aleatória
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        posicao_inicial = Position(x, y)

        # CRIAR O PERFIL DO PACIENTE
        print(f"[{self.agent.name}] A criar perfil do paciente...")
        
        # Guardamos no self.agent para que o CyclicBehaviour e o PeriodicBehaviour o vejam depois!
        self.agent.meu_perfil = Perfil_paciente(
            jid_paciente=str(self.agent.jid),
            nome=f"Paciente_{self.agent.name}", # Nome genérico baseado no JID
            doencas=["Diabetes", "Hipertensao", "DPOC"]  
        )
        
        # Atualizamos a posição no perfil criado
        self.agent.meu_perfil.posicao_atual = posicao_inicial

        # Preparar a Mensagem de Subscrição (Registo na Plataforma)
        destino = self.agent.get("service_contact")
        
        if destino:
            msg = Message(to=destino)
            msg.set_metadata("performative", "subscribe")
            
            # Enviamos o relatório inicial formatado para a plataforma saber quem somos e o que temos.
            dados_iniciais = self.agent.meu_perfil.formatar_relatorio()
            msg.body = jsonpickle.encode(dados_iniciais)

            await self.send(msg)
            print(f"[{self.agent.name}] Subscreveu à Plataforma ({destino}) com posição {x},{y}")
        else:
            print(f"[{self.agent.name}] ERRO: 'service_contact' não definido!")