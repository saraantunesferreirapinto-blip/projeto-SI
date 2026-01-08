from spade.agent import Agent
from Behaviour.cyclic_paciente import CyclicBehavPaciente
from Behaviour.oneShot_paciente import OneShotBehavPaciente
from Behaviour.periodic_paciente import PeriodicBehavPaciente

class CustomerAgent(Agent):

    taxis_subscribed = []

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPaciente()
        b = OneShotBehavPaciente()
        c = PeriodicBehavPaciente(period=1)
        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)

