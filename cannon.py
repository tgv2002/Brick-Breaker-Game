from heads import *
from component import *
from helper import *
from paddle import *

class Cannon(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__do_display = False
        
    def create_cannon(self):
        self.comp.append("XX")
    
    def can_display_cannon(self):
        return self.__do_display

    def set_display_status(self, stat):
        self.__do_display = stat
        
    def display_component(self):
        for i in range(len(self.comp)):
            for j in range(len(self.comp[i])):
                self.game_arena.arena[self._y + i][self._x + j] = Fore.BLUE + self.comp[i][j] + Style.RESET_ALL
                  
    def shoot_bullet(self):
        v_y = random.randint(-3, -1)
        v_x = random.randint(-2, 3)
        while v_x == 0:
            v_x = random.randint(-2, 3)
        return v_x, v_y