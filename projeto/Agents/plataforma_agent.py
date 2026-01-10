from spade.agent import Agent
from Behaviour.cyclic_plataforma import CyclicBehavPlataforma
from Behaviour.periodic_plataforma import PeriodicBehavPlataforma

class PlataformaAgent(Agent):
<<<<<<< HEAD
    paciente_subscribe = []
    medico_subscribe = []
    historico_falhas = {}
=======

    paciente_subscribe = []
    medico_subscribe = {}    
    historico_falhas = {}
    alertas_pendentes = {}
>>>>>>> 16c6eca93ada049ef1f74b99333fca7060631c42

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPlataforma()
        b = PeriodicBehavPlataforma(period=10)
        self.add_behaviour(a)
        self.add_behaviour(b)