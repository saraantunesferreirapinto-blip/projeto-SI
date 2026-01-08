import jsonpickle
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class PeriodicBehavDispositivo (PeriodicBehaviour):

    async def run(self):
        # Acede ao objeto lógico (Tensiometro/Glicometro) guardado no Agente
        dispositivo_logica = self.agent.dispositivo_logica
        # Gera os dados (Polimorfismo: funciona para qualquer classe)
        dados = dispositivo_logica.gerar_dados()

        # Envia para o JID que foi configurado no agente (o paciente/médico)
        msg = Message(to=self.agent.jid_paciente)
        msg.set_metadata("performative", "inform")
        
        # Ajuda o paciente a organizar os dados no dicionário
        msg.set_metadata("tipo_dispositivo", type(dispositivo_logica).__name__.lower())
        msg.body = jsonpickle.encode(dados)

        await self.send(msg)
        print(f"[{self.agent.name}] enviou {type(dispositivo_logica).__name__}: {dados}")