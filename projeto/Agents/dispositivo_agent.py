from spade.agent import Agent
from Behaviour.periodic_dispositivo import PeriodicBehavDispositivo

class DispositivoAgent(Agent):

    def __init__(self, jid, password, tipo_dispositivo, jid_paciente):
        super().__init__(jid, password)
        # Guardamos a lógica específica (o objeto Tensiometro ou Glicometro)
        self.tipo_dispositivo = tipo_dispositivo
        # Guardamos para quem este agente deve enviar os dados
        self.jid_paciente = jid_paciente

    async def setup(self):
        # Adiciona o comportamento para enviar dados a cada 5 segundos
        b = PeriodicBehavDispositivo(period=10)
        self.add_behaviour(b)