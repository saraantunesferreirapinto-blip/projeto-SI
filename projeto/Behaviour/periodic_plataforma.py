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
            
            # 1. FILTRAR: Manter apenas falhas que aconteceram na JANELA DE TEMPO
            falhas_recentes = [t for t in lista_timestamps if t > (agora - JANELA_TEMPO)]
            
            # Atualiza a lista do agente (apagando as velhas para não ocupar memória)
            self.agent.historico_falhas[paciente] = falhas_recentes
            
            qtd = len(falhas_recentes)

            # 2. VERIFICAR A CONDIÇÃO
            if qtd > LIMITE_FALHAS:
                print(f"ALERTA: O paciente {paciente} teve {qtd} falhas nos últimos {JANELA_TEMPO}s!")
                # Enviar email, SMS, etc.
            
            elif qtd > 0:
                print(f"   Info: {paciente} teve {qtd} falha (ainda dentro do limite).")