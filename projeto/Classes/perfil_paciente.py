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
        self.posicao_atual = None 

    def formatar_relatorio(self):

        pos_dict = None
        if self.posicao_atual and isinstance(self.posicao_atual, Position):
            pos_dict = {"x": self.posicao_atual.x, "y": self.posicao_atual.y}

        relatorio = {
            "paciente": self.nome,
            "jid": self.jid_paciente,
            "doenca" : self.doencas,
            "sinais_vitais": {},
            "posicao": pos_dict,
        }
    
        lista_doencas = [d.lower() for d in self.doencas]
        sinais = {}

        if "diabetes" in lista_doencas:
            sinais["glicometro"] = self.dados_glicometro
        
        if "hipertensao" in lista_doencas or "hipertensão" in lista_doencas:
            sinais["tensiometro"] = self.dados_tensiometro
            
        if "dpoc" in lista_doencas:
            sinais["oximetro"] = self.dados_oximetro 

        relatorio["sinais_vitais"] = sinais
        return relatorio
    
    def atualizar_sinal(self, tipo_dispositivo, valor):
        if tipo_dispositivo == "oximetro":
            self.dados_oximetro = valor
        elif tipo_dispositivo == "tensiometro":
            self.dados_tensiometro = valor
        elif tipo_dispositivo == "glicometro":
            self.dados_glicometro = valor