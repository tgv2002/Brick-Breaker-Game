from heads import *
from component import *
from helper import *
from powerUp import *
from ball import *

class FireBall(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        
    def create_fire_ball_power_up(self):
        self.comp.append("----")
        self.comp.append("|FB|")
        self.comp.append("----")
    
    def fire_ball(self, game_balls): 
        for game_ball in game_balls:
            if game_ball.can_display_ball() and not game_ball.get_movement_status():
                game_ball.set_fire_mode(True)
        self._is_activated = True
        self._do_display = False
    
    def remove_fire_ball(self, game_balls): 
        for game_ball in game_balls:
            if game_ball.can_display_ball() and not game_ball.get_movement_status():
                game_ball.set_fire_mode(False)
        self._is_activated = False