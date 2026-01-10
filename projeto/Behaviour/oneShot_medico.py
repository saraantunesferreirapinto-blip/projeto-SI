import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Classes.position import Position
import jsonpickle

class oneShotBehavMedico (OneShotBehaviour):
    async def run(self):

        x = random.randint(1, 100)
        y = random.randint(1, 100)
        self.agent.perfil.posicao_atual = Position(x, y)
        
        # Correção do Print: Aceder ao perfil e converter para string corretamente
        print(f"Agent {self.agent.jid}: Medico Agent initialized at Pos({x}, {y})")
        
        # 2. Preparar a mensagem para a Plataforma
        # Usamos o jid que passaste no main: self.agent.plataforma_jid
        msg = Message(to=str(self.agent.plataforma_jid))

        # Definimos a performativa como 'propose' porque é a que a tua Plataforma 
        # está à espera para registar médicos (visto no teu código da Plataforma)
        msg.set_metadata("performative", "propose")  # Instantiate the message

        msg.body = jsonpickle.encode(self.agent.perfil)               

        print(f"Agent {self.agent.jid}: Enviando proposta de serviço para a Plataforma...")
        
        await self.send(msg)