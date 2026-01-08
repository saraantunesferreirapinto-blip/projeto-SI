from spade.agent import Agent
from behaviour.cyclic_medico import CyclicBehavMedico

class CustomerAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavMedico()
        self.add_behaviour(a)
