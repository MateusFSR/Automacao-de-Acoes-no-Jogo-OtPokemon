

from utils import move_and_click


class HandlerPoke:
    
    def __init__(self):
        self.count = 0
        self.list_poke = [(90, 230), (90, 270), (90, 315), (90, 350), (90, 450)]#(90, 400)]
    
    def check_poke_leght(self):
        self.count = self.count % len(self.list_poke)

    def next(self):
        self.count = self.count + 1
        self.check_poke_leght()
        move_and_click(self.list_poke[self.count])
    
    def previous(self):
        self.count = self.count - 1
        self.check_poke_leght()
        move_and_click(self.list_poke[self.count])


poke = HandlerPoke()

