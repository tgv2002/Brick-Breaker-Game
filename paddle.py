from heads import *
from component import *
from helper import *
from ball import *

class Paddle(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena, paddle_length):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__paddle_length = paddle_length
        self.__grab_balls = True
        self.__do_display = True
        
    def get_paddle_length(self):
        return self.__paddle_length
    
    def can_grab_balls(self):
        return self.__grab_balls
    
    def set_grab_balls(self, stat):
        self.__grab_balls = stat
    
    def can_display_paddle(self):
        return self.__do_display
    
    def set_display_status(self, stat):
        self.__do_display = stat
        
    def move_component(self, direction, game_balls, game_cannon_1, game_cannon_2, game_boss_enemy, game_boss_enemy_unbreakable_bricks, LEVEL):
        units_to_move = 0
        if direction == 0:
            if self._x > (LEFT_OFFSET + 1):
                dist_from_left = self._x - LEFT_OFFSET
                if dist_from_left <= 3:
                    self._x = LEFT_OFFSET + 1
                    units_to_move = 1 - dist_from_left
                else:
                    self._x -= 3
                    units_to_move = -3
            else:
                os.system('aplay -q ./sound_effects/paddle_hit_wall.wav&')
           
        else:
            if self._x < (WIDTH - 3 - self.__paddle_length):
                dist_from_right = WIDTH - 1 - self._x - self.__paddle_length
                if dist_from_right <= 3:
                    self._x = (WIDTH - 2 - self.__paddle_length)
                    units_to_move = 1 - dist_from_right
                else:
                    self._x += 3
                    units_to_move = 3
            else:
                os.system('aplay -q ./sound_effects/paddle_hit_wall.wav&')
                
        for game_ball in game_balls:
            if game_ball.can_display_ball() and game_ball.get_movement_status():
                game_ball.set_x(game_ball.get_x() + units_to_move)
        game_cannon_1.set_x(game_cannon_1.get_x() + units_to_move)
        game_cannon_2.set_x(game_cannon_2.get_x() + units_to_move)
        if game_boss_enemy.can_display_boss_enemy():
            game_boss_enemy.move_component(self._x - 12)
        

    def set_paddle_length(self, leng):
        self.__paddle_length = leng
        self.comp.pop()
        new_pad = ""
        for i in range(leng):
            new_pad += "-"
        self.comp.append(new_pad)
                
    def create_paddle(self):
        pad = ""
        for i in range(self.__paddle_length):
            pad += "-"
        self.comp.append(pad)