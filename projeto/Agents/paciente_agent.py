from spade.agent import Agent
from Behaviour.cyclic_paciente import CyclicBehavPaciente
from Behaviour.oneShot_paciente import OneShotBehavPaciente
from Behaviour.periodic_paciente import PeriodicBehavPaciente

class PacienteAgent(Agent):

    def __init__(self, jid, password, perfil, jid_plataforma):
        super().__init__(jid, password)
        self.meu_perfil = perfil
        
        # CORRETO (Cria o atributo que o comportamento está à procura):
        self.jid_plataforma = jid_plataforma

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPaciente()
        b = OneShotBehavPaciente()
        c = PeriodicBehavPaciente(period=5)
        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)