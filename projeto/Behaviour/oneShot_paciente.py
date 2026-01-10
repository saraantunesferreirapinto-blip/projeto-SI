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

        
        # 2. USAR O PERFIL QUE VEIO DA MAIN
        # Em vez de criar um novo (o que apagaria o nome "Maria"),
        # nós apenas adicionamos a posição ao perfil que já existe!
        if hasattr(self.agent, "meu_perfil") and self.agent.meu_perfil:
            print(f"[{self.agent.name}] A definir posição inicial para {self.agent.meu_perfil.nome}...")
            self.agent.meu_perfil.posicao_atual = posicao_inicial
        else:
            print(f"[{self.agent.name}] ERRO CRÍTICO: Perfil não encontrado! (Verifique o __init__ do Agente)")
            return

        # 3. REGISTAR NA PLATAFORMA
        destino = self.agent.jid_plataforma # Acede diretamente à variável criada no __init__ 
        
        if destino:
            msg = Message(to=destino)
            msg.set_metadata("performative", "subscribe")
            
            # Enviamos o relatório inicial formatado para a plataforma saber quem somos e o que temos.
            msg.body = jsonpickle.encode(self.agent.meu_perfil)

            await self.send(msg)
            print(f"[{self.agent.name}] Subscreveu à Plataforma ({destino}) com posição {x},{y}")
        else:
            print(f"[{self.agent.name}] ERRO: 'service_contact' não definido!")