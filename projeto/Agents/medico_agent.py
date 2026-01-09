from spade.agent import Agent
from Behaviour.cyclic_medico import CyclicBehavMedico
from Behaviour.oneShot_medico import oneShotBehavMedico


class MedicoAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavMedico()
        b = oneShotBehavMedico()
        self.add_behaviour(a)
        self.add_behaviour(b)
