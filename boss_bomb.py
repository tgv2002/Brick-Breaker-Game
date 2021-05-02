from heads import *
from component import *
from helper import *
from paddle import *
from brick import *

class BossBomb(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__do_display = True
        
    def create_bomb(self):
       self.comp.append(" ,-*")
       self.comp.append("(_) ")
    
    def can_display_bomb(self):
        return self.__do_display

    def set_display_status(self, stat):
        self.__do_display = stat
        
    def display_component(self):                        
        if self.__do_display:
            for i in range(len(self.comp)):
                for j in range(len(self.comp[i])):
                    if self.comp[i][j] != '*':
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.RED + self.comp[i][j] + Style.RESET_ALL
                    else:
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.YELLOW + self.comp[i][j] + Style.RESET_ALL   
    
    def move_component(self, game_paddle):
        self._y += BOMB_DROP_VELOCITY  
        if self._y >= game_paddle.get_y():
            self.__do_display = False
            return self.collided(game_paddle)