from spade.behaviour import CyclicBehaviour
import jsonpickle
from spade.message import Message

class CyclicBehavPaciente(CyclicBehaviour):

    async def run(self):
        print("Paciente: À espera de dados...")

        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            
            if performative == "inform":
                # Descodifica o JSON
                conteudo = jsonpickle.decode(msg.body)

                tipo = conteudo.get("tipo_dispositivo")
                valor = conteudo.get("valor")
                remetente = msg.sender  # O JID de quem enviou (ex: tensiometro@server)

                print(f"--> Recebi dados de {remetente}: {tipo} = {valor}")

                # Atualiza a Classe Perfil (que está no Agente)
                self.agent.meu_perfil.atualizar_sinal(tipo, valor)

                # Verifica como ficou o relatório atual
                relatorio = self.agent.meu_perfil.formatar_relatorio()
                print(f"    Estado Atual do Paciente: {relatorio['sinais_vitais']}")

            elif performative == "failure":

                conteudo = jsonpickle.decode(msg.body)

                tipo = conteudo.get("tipo_dispositivo")
                valor = conteudo.get("valor")
                remetente = msg.sender  # O JID de quem enviou (ex: tensiometro@server)

                print(f"--> Recebi dados de {remetente}: {tipo} = {valor}")

                # Atualiza a Classe Perfil (que está no Agente)
                self.agent.meu_perfil.atualizar_sinal(tipo, valor)

                # Verifica como ficou o relatório atual
                relatorio = self.agent.meu_perfil.formatar_relatorio()
                print(f"    Estado Atual do Paciente: {relatorio['sinais_vitais']}")

                msg = Message(to=self.agent.jid_destino)
                msg.set_metadata("performative", "failure")
                msg.body = jsonpickle.encode(relatorio)

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")
        
        else:
            print("Paciente: Nenhuma mensagem recebida recentemente.")