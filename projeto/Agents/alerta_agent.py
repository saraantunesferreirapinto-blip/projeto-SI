from spade.agent import Agent
from Behaviour.cyclic_alerta import CyclicBehavAlerta

class AlertaAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavAlerta()
        self.add_behaviour(a)
