import random

from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Classes.informPosition import InformPosition
from Classes.position import Position
import jsonpickle

class oneShotBehavMedico (OneShotBehaviour):
    async def run(self):
        # using random.randint(a,b) to get a random int between a and b
        # use it to randomly initialize the position of the taxi in the map, i.e., between positions [1-100] for x axis and [1-100] for y axis
        self.agent.current_location = InformPosition(str(self.agent.jid), Position(random.randint(1, 100), random.randint(1, 100)), True)
        print("Agent {}:".format(str(self.agent.jid)) + " Medico Agent initialized with {}".format(self.agent.current_location.toString()))

        msg = Message(to=self.agent.get("service_contact"))             # Instantiate the message
        msg.body = jsonpickle.encode(self.agent.current_location)       # Set the message content (serialized object)
        msg.set_metadata("performative", "subscribe")                   # Set the message performative

        print("Agent {}:".format(str(self.agent.jid)) + " Taxi Agent subscribing to Manager Agent {}".format(str(self.agent.get("service_contact"))))
        await self.send(msg)