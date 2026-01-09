from spade.agent import Agent
from Behaviour.cyclic_paciente import CyclicBehavPaciente
from Behaviour.oneShot_paciente import OneShotBehavPaciente
from Behaviour.periodic_paciente import PeriodicBehavPaciente

class PacienteAgent(Agent):

    def __init__(self, jid, password, nome_paciente, doencas_paciente, jid_plataforma):
        super().__init__(jid, password)
        self.nome_inicial = nome_paciente
        self.doencas_inicial = doencas_paciente
        
        # Guardar o contacto da plataforma
        self.set("jid_plataforma", jid_plataforma)

    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavPaciente()
        b = OneShotBehavPaciente()
        c = PeriodicBehavPaciente(period=1)
        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)

