from spade.behaviour import CyclicBehaviour
import jsonpickle
from spade.message import Message

class CyclicBehavPaciente(CyclicBehaviour):

    async def run(self):

        msg = await self.receive(timeout=10)

        if msg:
            conteudo = jsonpickle.decode(msg.body)
            performative = msg.get_metadata("performative")

            if "recomendacao" in conteudo:
                medico = conteudo.get("medico", "Desconhecido")
                rec = conteudo.get("recomendacao")
                print(f"\n[NOTIFICAÇÃO MÉDICA] O médico {medico} recomenda: {rec}\n")


            elif performative == "inform" or performative is None:

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

                # Enviar para o GESTOR DE ALERTAS (para análise de risco)
                if hasattr(self.agent, "jid_alerta") and self.agent.jid_alerta:
                    msg_alert = Message(to=self.agent.jid_alerta)
                    msg_alert.set_metadata("performative", "inform")
                    msg_alert.body = jsonpickle.encode(relatorio) 
                    await self.send(msg_alert)
                    print(f"[Envio] Dados encaminhados para: {self.agent.jid_alerta}")

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

                msg = Message(to=self.agent.get("jid_plataforma"))
                msg.set_metadata("performative", "failure")
                msg.body = jsonpickle.encode(relatorio)

            elif performative == "agree":
                print(f"[{self.agent.name}] ✅ Confirmação recebida: {msg.body}")
                return

            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")
        
        else:
            print("Paciente: Nenhuma mensagem recebida recentemente.")

