from Classes.position import Position

class Perfil_medico:
<<<<<<< HEAD
    def _init_(self, jid_medico, nome, especialidade):
        self.jid_medico = jid_medico
        self.nome = nome
        self.especialidade = especialidade
=======
    def _init_(self, jid_medico: str, nome: str, especialidade: str, disponibilidade: bool, position: Position):
        self.jid_medico = jid_medico
        self.nome = nome
        self.especialidade = especialidade
        self.disponibilidade = disponibilidade
        self.posicao = position
>>>>>>> df5ac7bf128c51b70186a4fa2002e1b33ae42f7c

    def formatar_perfil(self):
        return {
            "medico": self.nome,
            "jid": self.jid_medico,
            "especialidade": self.especialidade,
            "posicao": Position,
<<<<<<< HEAD
=======
            "disponibilidade": self.disponibilidade
>>>>>>> df5ac7bf128c51b70186a4fa2002e1b33ae42f7c
        }