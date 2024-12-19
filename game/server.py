from twisted.internet import reactor
from twisted.spread import pb

from controllers import NetworkClientController
from models import Game
from patterns import NoTickMediator
from views import TextLogView

from preferences import PORT

def main():
    evt_mgr = NoTickMediator()

    log = TextLogView(evt_mgr) # view
    client_controller = NetworkClientController(evt_mgr) # controller
    game = Game(evt_mgr) # model
    reactor.listenTCP(PORT, pb.PBServerFactory(client_controller))
    reactor.run()

if __name__ == '__main__':
    main()
