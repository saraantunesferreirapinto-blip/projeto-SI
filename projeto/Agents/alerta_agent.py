from spade.agent import Agent
from Behaviour.cyclic_alerta import CyclicBehavAlerta

class AlertaAgent(Agent):

    # Precisamos de receber o médico e a plataforma aqui!
    def __init__(self, jid, password, plataforma_jid):
        super().__init__(jid, password)
        
        # Guardar na "memória" do agente para o Comportamento usar depois
        self.set("plataforma_jid", plataforma_jid)

    async def setup(self):
        a = CyclicBehavAlerta()
        self.add_behaviour(a)