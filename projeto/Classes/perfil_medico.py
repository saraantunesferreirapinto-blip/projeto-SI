from Classes.position import Position

class Perfil_medico:
    def _init_(self, jid_medico: str, nome: str, especialidade: str, disponibilidade: bool, position: Position):
        self.jid_medico = jid_medico
        self.nome = nome
        self.especialidade = especialidade
        self.disponibilidade = disponibilidade
        self.posicao = position

    def formatar_perfil(self):
        return {
            "medico": self.nome,
            "jid": self.jid_medico,
            "especialidade": self.especialidade,
            "posicao": Position,
            "disponibilidade": self.disponibilidade
        }