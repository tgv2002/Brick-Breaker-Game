from heads import *
from component import *
from helper import *
from powerUp import *
from paddle import *
from ball import *

class ShootingPaddle(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        
    def create_shooting_paddle_power_up(self):
        self.comp.append("----")
        self.comp.append("|SP|")
        self.comp.append("----")
    
    def shoot_from_paddle(self):
        self._is_activated = True
        self._do_display = False
            
    def remove_shooting_paddle(self):
        self._is_activated = False      