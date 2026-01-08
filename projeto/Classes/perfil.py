class Perfil:
    def __init__(self, jid_paciente, nome):
        self.jid_paciente = jid_paciente
        self.nome = nome
        self.dados_oximetro = None
        self.dados_tensiometro = None
        self.dados_glicometro = None

    def formatar_relatorio(self):
        return {
            "paciente": self.nome,
            "jid": self.jid_paciente,
            "sinais_vitais": {
                "oximetro": self.dados_oximetro,
                "tensiometro": self.dados_tensiometro, # "120/80"
                "glicometro": self.dados_glicometro
            }
        }