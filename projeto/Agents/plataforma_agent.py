from spade.agent import Agent
from Behaviour.cyclic_plataforma import CyclicBehavPlataforma
from Behaviour.periodic_plataforma import PeriodicBehavPlataforma

class PlataformaAgent(Agent):
    paciente_subscribe = []
    medico_subscribe = []
    historico_falhas = {}

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPlataforma()
        b = PeriodicBehavPlataforma(period=10)
        self.add_behaviour(a)
        self.add_behaviour(b)
