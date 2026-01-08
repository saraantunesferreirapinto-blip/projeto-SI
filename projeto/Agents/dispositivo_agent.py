from spade.agent import Agent
from Behaviour.periodic_dispositivo import PeriodicBehavDispositivo

class CustomerAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = PeriodicBehavDispositivo(period=1)
        self.add_behaviour(a)
