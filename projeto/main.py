import time
import spade
from spade import wait_until_finished

# Importação dos Agentes (Baseado na tua pasta 'Agents')
from Agents.plataforma_agent import PlataformaAgent
from Agents.medico_agent import MedicoAgent
from Agents.alerta_agent import AlertaAgent
from Agents.paciente_agent import PacienteAgent
from Agents.dispositivo_agent import DispositivoAgent

XMPP_SERVER = 'desktop-NIKN4PF'
PASSWORD = 'NOPASSWORD'

NUM_PACIENTES = 3

async def main():

    agentes_ativos = []
    
    print("--- A INICIAR SISTEMA DE TELESSAÚDE ---")

    # ---------------------------------------------------------
    # 1. INICIAR INFRAESTRUTURA CENTRAL (Plataforma, Médico, Alerta)
    # ---------------------------------------------------------
    
    # -- Agente Plataforma (Centraliza a informação) --
    plataforma_jid = f"plataforma@{XMPP_SERVER}"
    plataforma_agent = PlataformaAgent(plataforma_jid, PASSWORD)
    await plataforma_agent.start()
    agentes_ativos.append(plataforma_agent)
    print(f"Plataforma iniciada: {plataforma_jid}")

    # -- Agente Médico (Recebe os alertas graves) --
    medico_jid = f"medico_geral@{XMPP_SERVER}"
    medico_agent = MedicoAgent(medico_jid, PASSWORD)
    await medico_agent.start()
    agentes_ativos.append(medico_agent)
    print(f" Médico iniciado: {medico_jid}")

    # -- Agente Alerta (Analisa dados e encaminha para o médico) --
    # O Agente Alerta precisa de saber quem é o Médico para lhe enviar notificações
    alerta_jid = f"gestor_alertas@{XMPP_SERVER}"
    alerta_agent= AlertaAgent(alerta_jid, PASSWORD)
    alerta_agent.set("medico_jid", medico_jid) 
    await alerta_agent.start()
    agentes_ativos.append(alerta_agent)
    print(f" Gestor de Alertas iniciado: {alerta_jid}")

    # Informar a Plataforma de quem é o Agente de Alerta (para encaminhar dados brutos se necessário)
    plataforma_agent.set("alerta_jid", alerta_jid)

    # Pausa para garantir que a infraestrutura está online antes dos pacientes
    time.sleep(2)

    # ---------------------------------------------------------
    # 2. INICIAR PACIENTES E DISPOSITIVOS (Loop para 3 Pacientes)
    # ---------------------------------------------------------
    for i in range(1, NUM_PACIENTES + 1):
        
        # -- Agente Paciente --

        paciente_jid = 'paciente{}@'.format(str(i)) + XMPP_SERVER
        paciente_agent = PacienteAgent(paciente_jid, PASSWORD)
    
        # O Paciente tem de saber para onde enviar os dados (Plataforma)
        paciente_agent.set("plataforma_jid", plataforma_jid)
        
        await paciente_agent.start()
        agentes_ativos.append(paciente_agent)

    

        #-- Dispositivo 1: Tensiómetro --
        # Instancia a lógica (classe pura)
        logica_tensiometro = Tensiometro()
        jid_tens = f"tens_p{i}@{XMPP_SERVER}"
        
        # Cria o agente injetando a lógica e o destino (o próprio paciente)
        agente_tens = DispositivoAgent(
            jid=jid_tens, 
            password=PASSWORD,
            dispositivo_logica=logica_tensiometro,
            jid_destino=paciente_jid
        )
        await agente_tens.start()
        agentes_ativos.append(agente_tens)
        print(f"   > Tensiómetro ligado ({jid_tens}) -> a enviar para {paciente_jid}")

        # -- Dispositivo 2: Glicómetro --
        logica_glicometro = Glicometro()
        jid_glico = f"glico_p{i}@{XMPP_SERVER}"
        
        agente_glico = DispositivoAgent(
            jid=jid_glico, 
            password=PASSWORD, 
            dispositivo_logica=logica_glicometro,
            jid_destino=paciente_jid
        )
        await agente_glico.start()
        agentes_ativos.append(agente_glico)
        print(f"   > Glicómetro ligado ({jid_glico}) -> a enviar para {paciente_jid}")

        # Pequena pausa para não "entupir" o servidor XMPP com registos simultâneos
        time.sleep(1)

    print("\n>>> SISTEMA TOTALMENTE OPERACIONAL <<<")
    print("Pressiona CTRL+C para encerrar a simulação.")

    # Mantém o script a correr até o utilizador interromper
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        print("A encerrar agentes...")
        for agente in agentes_ativos:
            await agente.stop()
        print("Todos os agentes foram desligados.")

if __name__ == "__main__":
    spade.run(main())