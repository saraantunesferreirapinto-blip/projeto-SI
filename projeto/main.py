import time
from projeto.Classes.dispositivo import Tensiometro, Glicometro
from Agents.dispositivo_agent import DispositivoAgent

def main():
    # Definir o JID do Paciente (quem vai receber os dados)
    paciente_jid = "paciente_01@servidor" 

    # Criar os objetos lógicos (apenas dados e métodos internos)
    logica_tensiometro = Tensiometro()
    logica_glicometro = Glicometro()

    # Criar os Agentes SPADE
    # Agente 1: É um Tensiómetro
    agente_tens = DispositivoAgent(
        jid="dispositivo_tens@servidor", 
        password="pass", 
        dispositivo_logica=logica_tensiometro, # Injeta a lógica aqui
        jid_destino=paciente_jid
    )

    # Agente 2: É um Glicómetro
    agente_glico = DispositivoAgent(
        jid="dispositivo_glico@servidor", 
        password="pass", 
        dispositivo_logica=logica_glicometro, # Injeta a lógica aqui
        jid_destino=paciente_jid
    )

    # Iniciar os agentes
    future_t = agente_tens.start()
    future_g = agente_glico.start()

    future_t.result()
    future_g.result()

    print("Dispositivos ligados e a enviar dados...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agente_tens.stop()
        agente_glico.stop()
        print("Agentes parados.")

if __name__ == "__main__":
    main()