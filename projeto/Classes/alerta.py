import time

class Alerta:
    def __init__(self, agente_nome, performative, doenca, problema, valor, conteudo):
        # 1. Gera o ID automaticamente ao criar o objeto
        self.id_alerta = f"alert_{agente_nome}_{int(time.time()*1000)}_{doenca}"
        
        # 2. Guarda os dados
        self.tipo_alerta = performative.upper()
        self.doenca_detetada = doenca
        self.problema = problema
        self.valor = valor
        self.conteudo_completo = conteudo
        
        # Guardamos a performative aqui para ajudar no envio, mas não vai no body
        self._performative_envio = performative

    # Método para transformar em dicionário (para enviar por JSON sem erros)
    def dict(self):
        return {
            "id_alerta": self.id_alerta,
            "tipo_alerta": self.tipo_alerta,
            "doenca_detetada": self.doenca_detetada,
            "problema": self.problema,
            "valor": self.valor,
            "conteudo_completo": self.conteudo_completo
        }