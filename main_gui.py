from dashboard import UserInterface
from Model import Model
from protocols import Protocols
from phonebook import PhonebookType
from Controller import Controller


# gossip_model = Model(20, 3, 100, Protocols.ANY, PhonebookType.ALL)
# user_interface = UserInterface(gossip_model)

# user_interface.show()


if __name__ == '__main__':
    c = Controller()
    c.run()