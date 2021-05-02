from heads import *
from component import *
from helper import *
from paddle import *
from brick import *

class Bullet(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__do_display = True
        
    def create_bullet(self):
        self.comp.append("*")
    
    def can_display_bullet(self):
        return self.__do_display

    def set_display_status(self, stat):
        self.__do_display = stat
        
    def display_component(self):
        if self.__do_display:
            if self._x > LEFT_OFFSET and self._x < (WIDTH - 1) and self._y > TOP_OFFSET and self._y < (HEIGHT - 1):
                self.game_arena.arena[self._y][self._x] = Fore.YELLOW + self.comp[0][0] + Style.RESET_ALL         
    
    def move_component(self, moved_x, moved_y):  
        if (moved_x <= LEFT_OFFSET or moved_x >= (WIDTH - 1) or moved_y <= TOP_OFFSET):
            self.__do_display = False
        else:
            self._x = moved_x
            self._y = moved_y