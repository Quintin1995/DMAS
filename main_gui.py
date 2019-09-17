from dashboard import UserInterface
from model import Model
from protocols import Protocols
from phonebook import PhonebookType

gossip_model = Model(20, 3, 100, Protocols.ANY, PhonebookType.ALL)
user_interface = UserInterface(gossip_model)

user_interface.show()
