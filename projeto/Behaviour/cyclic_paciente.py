import spade
from spade.behaviour import CyclicBehaviour
import jsonpickle

class cyclic_paciente(CyclicBehaviour):

    async def run(self):
        print("Paciente: À espera de dados...")

        msg = await self.receive(timeout=10)

        if msg:
            try:
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

            except Exception as e:
                print(f"ERRO ao ler mensagem: {e}")
        
        else:
            print("Paciente: Nenhuma mensagem recebida recentemente.")