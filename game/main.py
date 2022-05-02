from controllers import (
    CPUSpinnerController,
    KeyboardController,
    KeyboardController2,
)
from models import Game
from patterns import Mediator
from views import MainView

def main():
    evt_mgr = Mediator()
    clock = CPUSpinnerController(evt_mgr) # controller 1
    # controller = KeyboardController(evt_mgr) # controller 2
    controller = KeyboardController2(evt_mgr) # controller 2
    view = MainView(evt_mgr) # view
    model = Game(evt_mgr) # model
    clock.run()

if __name__ == '__main__':
    main()
