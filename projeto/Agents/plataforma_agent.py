from spade.agent import Agent
from Behaviour.cyclic_plataforma import CyclicBehavPlataforma
from Behaviour.periodic_plataforma import PeriodicBehavPlataforma

<<<<<<< HEAD
class CustomerAgent(Agent):

    paciente_subscribe = []
    medico_subscribe = []
    historico_falhas = {}
=======
class PlataformaAgent(Agent):
    historico_falhas = {}

>>>>>>> 9c69ac535f643e34c35bdc31af9d5708352ed5d8
    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPlataforma()
        b = PeriodicBehavPlataforma(period=10)
        self.add_behaviour(a)
        self.add_behaviour(b)
