from Classes.position import Position

class Perfil_medico:
    def _init_(self, jid_medico, nome, especialidade):
        self.jid_medico = jid_medico
        self.nome = nome
        self.especialidade = especialidade

    def formatar_perfil(self):
        return {
            "medico": self.nome,
            "jid": self.jid_medico,
            "especialidade": self.especialidade,
            "posicao": Position,
        }