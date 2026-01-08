from spade.agent import Agent
from Behaviour.periodic_dispositivo import PeriodicBehavDispositivo
from projeto.Classes.tensiometro import Tensiometro

class DispositivoAgent(Agent):

    def __init__(self, jid, password, dispositivo_logica, jid_destino):
        super().__init__(jid, password)
        # Guardamos a lógica específica (o objeto Tensiometro ou Glicometro)
        self.dispositivo_logica = dispositivo_logica
        # Guardamos para quem este agente deve enviar os dados
        self.jid_destino = jid_destino

    async def setup(self):
        print(f"Agente {self.name} a iniciar...")
        # Adiciona o comportamento para enviar dados a cada 5 segundos
        b = PeriodicBehavDispositivo(period=5)
        self.add_behaviour(b)
