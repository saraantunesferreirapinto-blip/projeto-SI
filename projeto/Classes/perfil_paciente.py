from Classes.position import Position

class Perfil_paciente:
    def __init__(self, jid_paciente, nome, doencas):
        self.jid_paciente = jid_paciente
        self.nome = nome
        if isinstance(doencas, str):
            self.doencas = [doencas]
        else:
            self.doencas = doencas
        self.dados_oximetro = None
        self.dados_tensiometro = None
        self.dados_glicometro = None

    def formatar_relatorio(self):
        relatorio = {
            "paciente": self.nome,
            "jid": self.jid_paciente,
            "doenca" : self.doenca,
            "sinais_vitais": {},
            "posicao": Position
        }
    
        # Normalizamos tudo para minúsculas para facilitar a comparação
        lista_doencas = [d.lower() for d in self.doencas]
        
        # Dicionário temporário para acumular os sinais vitais necessários
        sinais = {}

        # Usamos IFs independentes (acumulativos)
        if "diabetes" in lista_doencas:
            sinais["glicometro"] = self.dados_glicometro
        
        if "hipertensao" in lista_doencas:
            sinais["        "] = self.dados_tensiometro
            
        if "dpoc" in lista_doencas:
            sinais["oxigenio"] = self.dados_oximetro

        relatorio["sinais_vitais"] = sinais
        return relatorio
    
        # Método auxiliar para atualizar dados facilmente a partir do Behaviour
    def atualizar_sinal(self, tipo_dispositivo, valor):
        if tipo_dispositivo == "oximetro":
            self.dados_oximetro = valor
        elif tipo_dispositivo == "tensiometro":
            self.dados_tensiometro = valor
        elif tipo_dispositivo == "glicometro":
            self.dados_glicometro = valor