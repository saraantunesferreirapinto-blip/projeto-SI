import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import random
import time

class PeriodicBehavPlataforma(PeriodicBehaviour):
    async def run(self):
        # CONFIGURAÇÃO DA REGRA
        JANELA_TEMPO = 30.0  
        LIMITE_FALHAS = 1  
        
        agora = time.time()
        print(f"[Verificador] A analisar falhas dos últimos {JANELA_TEMPO}s...")

        # Iterar sobre todos os pacientes com registo de falhas
        for paciente, lista_timestamps in list(self.agent.historico_falhas.items()):
            
            # FILTRAR: Manter apenas falhas que aconteceram na JANELA DE TEMPO
            falhas_recentes = [t for t in lista_timestamps if t > (agora - JANELA_TEMPO)]
            
            # Atualiza a lista do agente (apagando as velhas para não ocupar memória)
            self.agent.historico_falhas[paciente] = falhas_recentes
            
            qtd = len(falhas_recentes)

            # VERIFICAR A CONDIÇÃO
            if qtd > LIMITE_FALHAS:
                    print(f"ALERTA: O paciente {paciente} teve {qtd} falhas nos últimos {JANELA_TEMPO}s!")
                    
                    # Pegamos no conteúdo da falha mais recente (o último da lista)
                    dados_alerta = falhas_recentes[-1]["conteudo"]
                    
                    # Adicionar flag de emergência
                    dados_alerta["motivo_alerta"] = "Muitas falhas consecutivas"

                    if self.agent.medico_subscribe:
                        medico_alvo = self.agent.medico_subscribe[0].jid_medico 
                        
                        msg_para_medico = Message(to=str(medico_alvo))
                        msg_para_medico.set_metadata("performative", "critico")
                        msg_para_medico.body = jsonpickle.encode(dados_alerta)
                        
                        await self.send(msg_para_medico)
                        print(f" -> Alerta CRÍTICO enviado para {medico_alvo}")
            
            # ======================================================================
            # TAREFA 2: VERIFICAR TIMEOUTS DE MÉDICOS (Reenvio de Alertas)
            # ======================================================================
            TEMPO_LIMITE_RESPOSTA = 15.0 
            MAX_TENTATIVAS = 3

            for id_alerta, dados in list(self.agent.alertas_pendentes.items()):
                
                if dados["status"] == "pendente":
                    tempo_passado = agora - dados["ultima_tentativa"]
                    
                    if tempo_passado > TEMPO_LIMITE_RESPOSTA:
                        
                        if dados["tentativas"] < MAX_TENTATIVAS:
                            # --- REENVIO ---
                            print(f" [Watchdog] Alerta {id_alerta} sem resposta há {int(tempo_passado)}s. Reenviando (Tentativa {dados['tentativas']+1})...")
                            
                            dados["tentativas"] += 1
                            dados["ultima_tentativa"] = agora
                            
                            # Reconstruir mensagem
                            msg = Message(to=dados["medico_atual"])
                            # Usa a performative original guardada, ou 'urgente' como fallback
                            msg.set_metadata("performative", dados.get("performative_orig", "urgente"))
                            msg.body = jsonpickle.encode(dados["conteudo"])
                            
                            await self.send(msg)
                        
                        else:
                            # --- FALHA DEFINITIVA ---
                            print(f" [Watchdog] Alerta {id_alerta} FALHOU (Max tentativas excedido).")
                            dados["status"] = "falhado"


            print("Manutenção concluída\n")