import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import json
import asyncio

class CyclicBehavMedico(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "agree":
                print(f"[{self.agent.name}] ✅ Confirmação recebida: {msg.body}")
                return
            
            try:
                # --- 2. DESCODIFICAÇÃO ROBUSTA ---
                dados_recebidos = jsonpickle.decode(msg.body)
                
                # Proteção contra Double Encoding (String dentro de String)
                if isinstance(dados_recebidos, str):
                    try:
                        import json
                        dados_recebidos = jsonpickle.decode(dados_recebidos)
                        if isinstance(dados_recebidos, str):
                            dados_recebidos = json.loads(dados_recebidos)
                    except:
                        pass
                
                if not isinstance(dados_recebidos, dict):
                    print(f"⚠️ Erro: Recebi dados que não são um dicionário. Ignorando.")
                    return

                # --- 3. EXTRAÇÃO DE DADOS ---
                id_alerta_recebido = dados_recebidos.get("id_alerta")
                problema = dados_recebidos.get("doenca_detetada", "Desconhecida")
                
                # Tentar obter o perfil (com fallback)
                perfil_paciente = dados_recebidos.get("conteudo_completo")
                if not perfil_paciente:
                    perfil_paciente = dados_recebidos.get("perfil_completo", {})

                # --- 4. ANÁLISE CLÍNICA (DEFINIR A RECOMENDAÇÃO) ---
                recomendacao = None
                
                if performative == "informativo":
                    recomendacao = "Manter monitorização e hidratação."
                elif performative == "urgente":
                    recomendacao = "Ajustar medicação. Contacto telefónico necessário."
                elif performative == "critico":
                    recomendacao = "URGENTE: Encaminhar para hospital imediatamente."

                # --- 5. ENVIO DA RESPOSTA (SÓ SE HOUVER RECOMENDAÇÃO) ---
                if recomendacao:
                    # Simular tempo de pensamento (opcional)
                    await asyncio.sleep(2)
                    
                    print(f"   Dr. Analisou: '{problema}' -> Rx: {recomendacao}")

                    payload_resposta = {
                        "id_alerta": id_alerta_recebido,
                        "acao_recomendada": recomendacao,
                        "medico_responsavel": str(self.agent.jid),
                        "dados_originais": dados_recebidos,
                        "perfil_completo": perfil_paciente
                    }

                    # USAR make_reply() É O SEGREDO
                    # Ele responde automaticamente para quem enviou (a Plataforma)
                    msg_resposta = msg.make_reply()
                    msg_resposta.set_metadata("performative", "request")
                    msg_resposta.body = jsonpickle.encode(payload_resposta)

                    await self.send(msg_resposta)
                    print(f" [{self.agent.name}] Parecer enviado com sucesso.")
            
            except Exception as e:
                print(f"❌ ERRO no Médico: {e}")
                print(f"   Conteúdo problemático: {msg.body}")