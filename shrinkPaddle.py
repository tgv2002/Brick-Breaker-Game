from heads import *
from component import *
from helper import *
from powerUp import *
from paddle import *

class ShrinkPaddle(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__leng_diff = 0
        
    def create_shrink_paddle_power_up(self):
        self.comp.append("-----")
        self.comp.append("| S |")
        self.comp.append("-----")
    
    def shrink_paddle(self, game_paddle):
        curr_leng = game_paddle.get_paddle_length()
        new_leng = int(round(curr_leng * 0.7))
        if new_leng <= 3:
            new_leng = 3
        game_paddle.set_paddle_length(new_leng)
        self.__leng_diff = curr_leng - new_leng
        self._is_activated = True
        self._do_display = False
            
    def remove_shrink_paddle(self, game_paddle):
        if self._is_activated:
            game_paddle.set_paddle_length(game_paddle.get_paddle_length() + self.__leng_diff)
            self._is_activated = False