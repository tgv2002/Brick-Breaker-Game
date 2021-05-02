from heads import *
from component import *
from helper import *
from powerUp import *
from paddle import *

class ExpandPaddle(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__leng_diff = 0
        
    def create_expand_paddle_power_up(self):
        self.comp.append("-----")
        self.comp.append("| E |")
        self.comp.append("-----")
    
    def expand_paddle(self, game_paddle):
        curr_leng = game_paddle.get_paddle_length()
        new_leng = int(round(curr_leng * 1.3))
        if new_leng >= WIDTH - 3 - LEFT_OFFSET:
            new_leng = WIDTH - 3 - LEFT_OFFSET
        self.__leng_diff = new_leng - curr_leng
        game_paddle.set_paddle_length(new_leng)
        if game_paddle.get_x() + new_leng > WIDTH - 1:
            game_paddle.set_x(WIDTH - 2 - new_leng)
        self._is_activated = True
        self._do_display = False

    def remove_expand_paddle(self, game_paddle):
        curr_leng = game_paddle.get_paddle_length()
        game_paddle.set_paddle_length(curr_leng - self.__leng_diff)
        self._is_activated = False