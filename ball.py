from heads import *
from component import *
from helper import *
from paddle import *

class Ball(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__stay_on_paddle = True
        self.__in_power_mode = False
        self.__in_fire_mode = False
        self.__do_display = True
        
    def create_ball(self):
        self.comp.append("O")
    
    def can_display_ball(self):
        return self.__do_display

    def set_display_status(self, stat):
        self.__do_display = stat
        
    def display_component(self):
        if self.__do_display:
            if self._x > LEFT_OFFSET and self._x < (WIDTH - 1) and self._y > TOP_OFFSET and self._y < (HEIGHT - 1):
                self.game_arena.arena[self._y][self._x] = Fore.WHITE + self.comp[0][0] + Style.RESET_ALL
        
    def get_movement_status(self):
        return self.__stay_on_paddle

    def ball_did_hit_paddle(self, game_paddle, dist_centre):
        self._vel_x += dist_centre
        self._vel_y *= -1 
    
    def paddle_check(self, moved_x, moved_y, game_paddle):
        # handles collisions between ball and paddle
        self._x = moved_x
        self._y = moved_y

        if self.collided(game_paddle):
            paddle_centre_x = (2*game_paddle.get_x() + game_paddle.get_paddle_length()) // 2
            if not game_paddle.can_grab_balls():
                self.ball_did_hit_paddle(game_paddle, moved_x - paddle_centre_x)
            else:
                self._y = game_paddle.get_y() - 1
                self.__stay_on_paddle = True
                self.ball_did_hit_paddle(game_paddle, moved_x - paddle_centre_x)
            return 2
        return 1
    
    def ball_reflection(self, obj, x1, y1):
        X1 = obj.get_x()
        X2 = obj.get_x() + len(obj.comp[0])
        Y1 = obj.get_y()
        Y2 = obj.get_y() + len(obj.comp)
        x2 = self._x
        y2 = self._y
        # self._x = INF
        # self._y = INF
        if y1 < Y1:
            # self._y = Y1 - 1
            self._vel_y *= -1
        elif y1 >= Y2:
            # self._y = Y2 
            self._vel_y *= -1
        elif x1 < X1:
            # self._x = X1 - 1
            self._vel_x *= -1
        else:
            # self._x = X2
            self._vel_x *= -1
        # if self._y == INF:
        #     if x2 != x1:
        #         self._y = int(round(((y2 - y1)*(self._x - x1))/(x2 - x1) + y1))
        #     else:
        #         if y1 > y2:
        #             self._y = Y2
        #         else:
        #             self._y = Y1 - 1
        # else:
        #     if y2 != y1:
        #         self._x = int(round(((x2 - x1)*(self._y - y1))/(y2 - y1) + x1))
        #     else:
        #         if x1 > x2:
        #             self._x = X2
        #         else:
        #             self._x = X1 - 1         
            
    
    def move_component(self, moved_x, moved_y, game_paddle):     
        if (moved_x <= LEFT_OFFSET or moved_x >= (WIDTH - 1)):
            if moved_x <= LEFT_OFFSET:
                self._x = LEFT_OFFSET + 1
            else:
                self._x = WIDTH - 2
            self._vel_x *= -1
            return 0
        elif moved_y <= TOP_OFFSET:
            self._vel_y *= -1
            self._y = TOP_OFFSET + 1
            return 0
        elif moved_y >= (game_paddle.get_y() + 6):
            self.__do_display = False
            return 0 
        else:
            return self.paddle_check(moved_x, moved_y, game_paddle)
    
    def is_in_power_mode(self):
        return self.__in_power_mode
    
    def set_power_mode(self, mode):
        self.__in_power_mode = mode

    def is_in_fire_mode(self):
        return self.__in_fire_mode
    
    def set_fire_mode(self, mode):
        self.__in_fire_mode = mode
    
    def update_movement_status(self, can_stay):
        self.__stay_on_paddle = can_stay