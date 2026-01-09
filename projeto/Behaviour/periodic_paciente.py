import jsonpickle
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Classes.perfil_paciente import Perfil_paciente

class PeriodicBehavDispositivo (PeriodicBehaviour):

    async def run(self):
        # ACEDER À INSTÂNCIA (O objeto real guardado no Agente)
        perfil = self.agent.meu_perfil
        
        if not perfil:
            return

        # OBTER OS DADOS (Usar o método que filtra as doenças)
        dados_para_enviar = perfil.formatar_relatorio()

        # CRIAR MENSAGEM
        msg_plataforma = Message(to=self.agent.jid_alerta)
        msg_plataforma.set_metadata("performative", "inform")
        
        # CODIFICAR OS DADOS REAIS
        msg_plataforma.body = jsonpickle.encode(dados_para_enviar)
        
        await self.send(msg_plataforma)
        print(f"[{self.agent.name}] Relatório enviado para o Agente Plataforma: {dados_para_enviar}")