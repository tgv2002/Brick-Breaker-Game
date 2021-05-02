from heads import *
from component import *
from helper import *
from powerUp import *
from ball import *

class BallMultiplier(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        
    def create_ball_multiplier_power_up(self):
        self.comp.append("----")
        self.comp.append("|x2|")
        self.comp.append("----")
    
    def multiply_ball(self, game_ball):
        self._is_activated = True
        self._do_display = False
        v_x = 0
        v_y = 0
        if game_ball.get_vel_x() >= 0:
            while v_x == 0:
                v_x = random.randint(-1 * (game_ball.get_vel_x()), game_ball.get_vel_x() + 1)
        else:
            while v_x == 0:
                v_x = random.randint(game_ball.get_vel_x(), (-1*game_ball.get_vel_x()) + 1)
        if game_ball.get_vel_y() >= 0:
            v_y = random.randint(-1*(game_ball.get_vel_y() + 1), -1)
        else:
            v_y = random.randint(game_ball.get_vel_y() - 1, -1)
        return v_x, v_y