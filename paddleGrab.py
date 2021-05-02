from heads import *
from component import *
from helper import *
from powerUp import *
from paddle import *
from ball import *

class PaddleGrab(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        
    def create_paddle_grab_power_up(self):
        self.comp.append("-----")
        self.comp.append("| G |")
        self.comp.append("-----")
    
    def paddle_grab(self, game_paddle):
        game_paddle.set_grab_balls(True)
        self._is_activated = True
        self._do_display = False
            
    def remove_paddle_grab(self, game_paddle):
        game_paddle.set_grab_balls(False)
        self._is_activated = False      