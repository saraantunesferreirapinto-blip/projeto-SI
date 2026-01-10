from spade.agent import Agent
from Behaviour.cyclic_medico import CyclicBehavMedico
from Behaviour.oneShot_medico import oneShotBehavMedico


class MedicoAgent(Agent):

    def __init__(self, jid, password, perfil, plataforma_jid):
        super().__init__(jid, password)
        self.perfil = perfil
        self.plataforma_jid = plataforma_jid
<<<<<<< HEAD

=======
        
>>>>>>> 4e85d73f58f2eaf98d9876a8751dbf49e19c3aee
    async def setup(self):
        print(f"agente customer iniciado: {self.jid}")
        a = CyclicBehavMedico()
        b = oneShotBehavMedico()
        self.add_behaviour(a)
        self.add_behaviour(b)
