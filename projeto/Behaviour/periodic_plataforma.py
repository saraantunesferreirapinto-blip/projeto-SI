import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import random
import time

class VerificaFalhasBehav(PeriodicBehaviour):
    async def run(self):
        # Limite de tolerância: 20 segundos sem dar sinais de vida
        TEMPO_LIMITE = 20.0 
        agora = time.time()
        
        # Iterar sobre todos os pacientes conhecidos
        # Usamos list() para evitar erros se o dicionário mudar durante o loop
        for paciente_jid, ultimo_tempo in list(self.agent.ultimos_contactos.items()):
            
            diferenca = agora - ultimo_tempo
            
            if diferenca > TEMPO_LIMITE:
                print(f"[ALERTA CRÍTICO] Perda de contacto com {paciente_jid}!")
                print(f"   -> O paciente não comunica há {int(diferenca)} segundos.")
                