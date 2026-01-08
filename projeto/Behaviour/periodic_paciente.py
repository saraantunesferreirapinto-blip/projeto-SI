import jsonpickle
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class PeriodicBehavDispositivo (PeriodicBehaviour):

    async def enviar_para_plataforma(self):

        if perfil.dados_oximetro and perfil.dados_tensiometro and perfil.dados_glicometro:
                await self.enviar_para_plataforma(perfil.formatar_relatorio())
                perfil.dados_oximetro = perfil.dados_tensiometro = perfil.dados_glicometro = None
                
        # Cria a mensagem agregada para a Plataforma
        msg_plataforma = Message(to=self.agent.jid_plataforma)
        msg_plataforma.set_metadata("performative", "inform")
        msg_plataforma.body = jsonpickle.encode(self.agent.dados_atuais)
        
        await self.send(msg_plataforma)
        print(f"[{self.agent.name}] Dados enviados para o Agente Plataforma!")