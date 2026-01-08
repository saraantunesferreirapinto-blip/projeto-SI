from spade.agent import Agent
from behaviour.cyclic_alerta import CyclicBehavAlerta

class CustomerAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavAlerta()
        self.add_behaviour(a)
