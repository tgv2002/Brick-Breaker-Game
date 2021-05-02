from heads import *
from component import *
from helper import *

class PowerUp(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self._do_display = True
        self._is_activated = False
        self._active_time = 0
        
    def move_component(self, game_paddle):
        moved_x = self._x + self._vel_x
        moved_y = self._y + self._vel_y
        if (moved_x <= LEFT_OFFSET or moved_x >= (WIDTH - 4)):
            if moved_x <= LEFT_OFFSET:
                self._x = LEFT_OFFSET + 1
            else:
                self._x = WIDTH - 5
            self._vel_x *= -1
            os.system('aplay -q ./sound_effects/paddle_hit_wall.wav&')
            return False
        elif moved_y <= TOP_OFFSET:
            self._vel_y *= -1
            self._y = TOP_OFFSET + 1
            os.system('aplay -q ./sound_effects/paddle_hit_wall.wav&')
            return False
        elif moved_y >= (game_paddle.get_y() - len(self.comp)):
            self._do_display = False
            self._x = moved_x
            self._y = (game_paddle.get_y() - len(self.comp))
            collided_paddle = self.collided(game_paddle)
            if not collided_paddle:
                os.system('aplay -q ./sound_effects/paddle_hit_wall.wav&')     
            return collided_paddle
        else:
            self._x = moved_x
            self._y = moved_y
            return False
            
    def get_elapsed_time(self):
        return self._active_time
    
    def set_elapsed_time(self, val):
        self._active_time = val
        
    def can_display_power_up(self):
        return self._do_display
    
    def set_display_status(self, stat):
        self._do_display = stat
        
    def is_active(self):
        return self._is_activated
    
    def set_active_status(self, stat):
        self._is_activated = stat
        