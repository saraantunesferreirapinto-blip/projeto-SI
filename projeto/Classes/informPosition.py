from Classes.position import Position


class InformPosition:
    def __init__(self, agent_jid: str, position: Position, available: bool):
        self.agent_jid = agent_jid
        self.position = position
        self.available = available

    def getAgent(self):
        return self.agent_jid

    def getPosition(self):
        return self.position

    def setPosition(self, x: int, y: int):
        self.position = Position(x, y)

    def setPosition(self, position: Position):
        self.position = position

    #def isAvailable(self):
    #    return self.available

    #def setAvailable(self, available: bool):
    #    self.available = available

    def toString(self):
        return "InformPosition [agent_jid=" + self.agent_jid + ", position=" + self.position.toString() + ", available=" + str(
            self.available) + "]"