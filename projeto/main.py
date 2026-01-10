import asyncio
import time
from Agents.plataforma_agent import PlataformaAgent
from Agents.alerta_agent import AlertaAgent
from Agents.medico_agent import MedicoAgent
from Agents.paciente_agent import PacienteAgent
from Agents.dispositivo_agent import DispositivoAgent

# Perfis e classes
from Classes.perfil_paciente import Perfil_paciente 
from Classes.perfil_medico import Perfil_medico 


XMPP_SERVER = 'laptop-rgqb7m90'
PASSWORD = 'NOPASSWORD'

async def criar_paciente_terminal(XMPP_SERVER, PASSWORD, id_sugestao):
    print(f"\n--- Configuração do Paciente {id_sugestao} ---")
    nome = input(f"Nome do Paciente: ")
    paciente_jid = f"paciente_{id_sugestao}@{XMPP_SERVER}"

    print("Selecione patologias (ex: 1,3): 1:Diabetes | 2:Hipertensão | 3:DPOC")
    escolhas = input("Patologias: ")
    
    lista_doencas = []

    mapa = {
        "1": "diabetes", 
        "2": "hipertensao", 
        "3": "dpoc"
    }

    for item in escolhas.split(','):
        ch = item.strip()
        if ch in mapa:
            nome_d = mapa[ch]
            lista_doencas.append(nome_d)

    for doenca in lista_doencas:
        tipo_sensor = ""
        if doenca == "diabetes": tipo_sensor = "glicometro"
        elif doenca == "hipertensao": tipo_sensor = "tensiometro" 
        elif doenca == "dpoc": tipo_sensor = "oximetro"
        
        if tipo_sensor:
            # Cria um nome único para o dispositivo
            dev_jid = f"{tipo_sensor}_{id_sugestao}@{XMPP_SERVER}"
            # O dispositivo tem de saber para quem enviar (paciente_jid)
            dev_agent = DispositivoAgent(dev_jid, PASSWORD, tipo_sensor, paciente_jid)
            await dev_agent.start()
            print(f"   -> Dispositivo {tipo_sensor} ativado.")

    perfil = Perfil_paciente(paciente_jid, nome=nome, doencas=lista_doencas)
    
    plat_jid = f"plataforma@{XMPP_SERVER}"

    # Passar tudo no construtor como definiste na classe
    paciente_agent = PacienteAgent(paciente_jid, PASSWORD, perfil, plat_jid)
    
    paciente_agent.jid_alerta = f"gestor_alertas@{XMPP_SERVER}"
    
    await paciente_agent.start()
    return [paciente_agent]

async def main():
    agentes_ativos = []

    # --- PLATAFORMA ---
    plataforma_jid = f"plataforma@{XMPP_SERVER}"
    plataforma_agent = PlataformaAgent(plataforma_jid, PASSWORD)
    
    # INJEÇÃO: Inicializar as variáveis que a plataforma precisa
    plataforma_agent.ultimos_contactos = {}
    plataforma_agent.falhas_consecutivas = {}
    plataforma_agent.historico_falhas = {}
    
    await plataforma_agent.start()
    agentes_ativos.append(plataforma_agent)
    print(f"Plataforma iniciada: {plataforma_jid}")

    # --- ALERTA ---
    alerta_jid = f"gestor_alertas@{XMPP_SERVER}"
    
    alerta_agent = AlertaAgent(alerta_jid, PASSWORD, plataforma_jid)
    
    await alerta_agent.start()
    agentes_ativos.append(alerta_agent) # Adicionar à lista
    print(f"Gestor de Alertas iniciado: {alerta_jid}")

    print("A iniciar Sistema...")
    
    # Mínimo 3 Pacientes 
    print("\n O sistema requer a configuração inicial de pelo menos 3 pacientes.")
    for i in range(1, 4):
        novos_agentes = await criar_paciente_terminal(XMPP_SERVER, PASSWORD, i)
        agentes_ativos.extend(novos_agentes)

    print("\n 3 pacientes cridispositivo_agentos. Sistema em execução.")

    # Menu de Gestão (Médicos e Pacientes dispositivo_agenticionais)
    try:
        while True:
            print("\n[MENU] 1: dispositivo_agenticionar Médico | 2: dispositivo_agenticionar Paciente | 3: Sair")
            opcao = await asyncio.get_event_loop().run_in_executor(None, input, "Escolha: ")

            if opcao == "1":
                nome_med = input("Nome do Médico: ")
                especialidade = input("Especialidade (ex: Cardiologia): ")
                
                medico_jid = f"medico_{nome_med.lower()}@{XMPP_SERVER}"

                perfil_med = Perfil_medico(
                    jid_medico=medico_jid, 
                    nome=nome_med, 
                    especialidade=especialidade
                )
                
                # Inicializar o Agente Médico
                medico_agent = MedicoAgent(medico_jid, PASSWORD, perfil=perfil_med)
                
                await medico_agent.start()
                agentes_ativos.append(medico_agent)
                
                print(f"Médico {nome_med} ({especialidade}) registado com sucesso.")
                
                time.sleep(1)

            elif opcao == "2":
                novo_id = len([a for a in agentes_ativos if isinstance(a, PacienteAgent)]) + 1
                novos = await criar_paciente_terminal(XMPP_SERVER, PASSWORD, novo_id)
                agentes_ativos.extend(novos)

            elif opcao == "3":
                break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        print("A encerrar agentes...")
        for agente in agentes_ativos:
            await agente.stop()
        print("Todos os agentes foram desligdispositivo_agentos.")

if __name__ == "__main__":
    asyncio.run(main())