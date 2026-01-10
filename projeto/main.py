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




XMPP_SERVER = 'WIN-SVIKB6A0MOG'
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
            print(f"Dispositivo {tipo_sensor} ativado.")

    perfil = Perfil_paciente(paciente_jid, nome=nome, doencas=lista_doencas)
    
    plat_jid = f"plataforma@{XMPP_SERVER}"
    alerta_jid = f"gestor_alertas@{XMPP_SERVER}"

    # Passar tudo no construtor como definiste na classe
    paciente_agent = PacienteAgent(paciente_jid, PASSWORD, perfil, plat_jid, alerta_jid)
    
    paciente_agent.jid_alerta = f"gestor_alertas@{XMPP_SERVER}"
    
    await paciente_agent.start()
    return [paciente_agent]

async def criar_equipa_medica(plataforma_jid):
    print("\n--- A INICIAR EQUIPA MÉDICA ---")
    
    # Lista de Médicos a criar (2 por especialidade)
    # Estrutura: (Nome, Especialidade)
    equipa = [
        ("Dr. Silva", "Endocrinologia"),   # Para Diabetes
        ("Dra. Santos", "Endocrinologia"), # Para Diabetes (Backup)
        
        ("Dr. Costa", "Cardiologia"),      # Para Hipertensão
        ("Dra. Pereira", "Cardiologia"),   # Para Hipertensão (Backup)
        
        ("Dr. Oliveira", "Pneumologia"),   # Para DPOC
        ("Dra. Ferreira", "Pneumologia")   # Para DPOC (Backup)
    ]

    agentes_medicos = []

    for nome, especialidade in equipa:
        # Criar um JID único sem espaços
        user_id = f"medico_{nome.lower().replace(' ', '').replace('.', '')}"
        medico_jid = f"{user_id}@{XMPP_SERVER}"

        # Criar o Perfil
        perfil_med = Perfil_medico(
            jid_medico=medico_jid, 
            nome=nome, 
            especialidade=especialidade
        )
        
        # Inicializar Agente
        medico_agent = MedicoAgent(medico_jid, PASSWORD, perfil=perfil_med, plataforma_jid=plataforma_jid)
        
        await medico_agent.start()
        agentes_medicos.append(medico_agent)
        
        # Pequena pausa para não "encavalar" os registos na consola
        await asyncio.sleep(0.2) 
        
    print("------------------------------------------------\n")
    return agentes_medicos

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

    # 3. INICIAR EQUIPA MÉDICA (AUTOMÁTICO) 🚑
    medicos = await criar_equipa_medica(plataforma_jid)
    agentes_ativos.extend(medicos)
    
    # Esperar um pouco para garantir que todos os médicos se registam na plataforma
    print("⏳ A aguardar registo dos médicos na rede...")
    await asyncio.sleep(2)

    print("A iniciar Sistema...")
    
    # Mínimo 3 Pacientes 
    print("\n O sistema requer a configuração inicial de pelo menos 3 pacientes.")
    for i in range(1, 4):
        novos_agentes = await criar_paciente_terminal(XMPP_SERVER, PASSWORD, i)
        agentes_ativos.extend(novos_agentes)

    print("\n 3 pacientes criados. Sistema em execução.")
    await asyncio.sleep(1)
    
if __name__ == "__main__":
    asyncio.run(main())