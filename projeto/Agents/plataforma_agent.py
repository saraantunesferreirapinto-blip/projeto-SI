from spade.agent import Agent
from behaviour.cyclic_plataforma import CyclicBehavPlataforma
from behaviour.periodic_plataforma import PeriodicBehavPlataforma

class CustomerAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPlataforma()
        b = PeriodicBehavPlataforma(period=10)
        self.add_behaviour(a)
        self.add_behaviour(b)
