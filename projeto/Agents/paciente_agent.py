from spade.agent import Agent
from behaviour.cyclic_paciente import CyclicBehavPaciente
from behaviour.oneShot_paciente import OneShotBehavPaciente
from behaviour.periodic_paciente import PeriodicBehavPaciente

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

