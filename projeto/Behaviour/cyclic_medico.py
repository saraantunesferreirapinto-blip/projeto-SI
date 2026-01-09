import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.message import Message


class cyclic_medico(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            if performative == "informativo":
                msg_plataforma = Message(to=self.agent.jid_plataforma)
                msg_plataforma.set_metadata("performative", "propose")
                msg_plataforma.body = ("Recomendação terapêutica")
                
                await self.send(msg_plataforma)
                print(f"[{self.agent.name}] Mensagem enviada para o Agente Plataforma!")

            elif performative == "urgente": 
                msg_plataforma = Message(to=self.agent.jid_plataforma)
                msg_plataforma.set_metadata("performative", "propose")
                msg_plataforma.body = ("Contacto com o paciente")
                
                await self.send(msg_plataforma)
                print(f"[{self.agent.name}] Mensagem enviada para o Agente Plataforma!")

            elif performative == "critico":    
                msg_plataforma = Message(to=self.agent.jid_plataforma)
                msg_plataforma.set_metadata("performative", "propose")
                msg_plataforma.body = ("Pedido de observação presencial")
                
                await self.send(msg_plataforma)
                print(f"[{self.agent.name}] Mensagem enviada para o Agente Plataforma!")