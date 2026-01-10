from Classes.position import Position

class Perfil_medico:
    def __init__(self, jid_medico: str, nome: str, especialidade: str, disponibilidade: bool, position: Position):
        self.jid_medico = jid_medico
        self.nome = nome
        self.especialidade = especialidade
        self.disponibilidade = disponibilidade
        self.posicao = position

    def formatar_perfil(self):

        pos_dict = None
        if self.posicao_atual and isinstance(self.posicao_atual, Position):
            pos_dict = {"x": self.posicao_atual.x, "y": self.posicao_atual.y}

        return {
            "medico": self.nome,
            "jid": self.jid_medico,
            "especialidade": self.especialidade,
            "posicao": pos_dict,
            "disponibilidade": self.disponibilidade
        }