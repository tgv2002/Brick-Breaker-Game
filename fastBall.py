from heads import *
from component import *
from helper import *
from powerUp import *
from ball import *

class FastBall(PowerUp):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__diff_x = 0
        self.__diff_y = 0
        
    def create_fast_ball_power_up(self):
        self.comp.append("-----")
        self.comp.append("| F |")
        self.comp.append("-----")
    
    def fasten_ball(self, game_balls):
        # for all balls 
        for game_ball in game_balls:
            if game_ball.can_display_ball() and not game_ball.get_movement_status():
                prev_vel_x = game_ball.get_vel_x()
                prev_vel_y = game_ball.get_vel_y()
                new_vel_x = int(round(prev_vel_x * 1.3))
                new_vel_y = int(round(prev_vel_y * 1.3))
                if new_vel_x >= 6:
                    new_vel_x = 6
                elif new_vel_x <= -6:
                    new_vel_x = -6
                if new_vel_y >= 6:
                    new_vel_y = 6
                elif new_vel_y <= -6:
                    new_vel_y = -6  
                game_ball.set_vel_x(new_vel_x)
                game_ball.set_vel_y(new_vel_y)
                self.__diff_x = new_vel_x - prev_vel_x
                self.__diff_y = new_vel_y - prev_vel_y
        self._is_activated = True
        self._do_display = False
                    
    def remove_fasten_ball(self, game_balls):
        for game_ball in game_balls:
            if game_ball.can_display_ball() and not game_ball.get_movement_status():
                game_ball.set_vel_x(game_ball.get_vel_x() - self.__diff_x)
                game_ball.set_vel_y(game_ball.get_vel_y() - self.__diff_y)
        self._is_activated = False
        