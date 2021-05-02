from heads import *
from helper import *

class Component:
    def __init__(self, x, y, color, vel_x, vel_y, game_arena):
        self.comp = []
        self._x = x
        self._y = y
        self._color = color
        self._vel_x = vel_x
        self._vel_y = vel_y
        self.game_arena = game_arena
        
    def set_x(self, x):
        self._x = x
    def get_x(self):
        return self._x
    
    def set_color(self, col):
        self._color = col
    
    def set_y(self, y):
        self._y = y
    def get_y(self):
        return self._y

    def set_vel_x(self, vx):
        self._vel_x = vx
    def get_vel_x(self):
        return self._vel_x
    
    def set_vel_y(self, vy):
        self._vel_y = vy
    def get_vel_y(self):
        return self._vel_y
    
    def collided(self, comp2):
        x_l1 = len(self.comp[0])
        y_l1 = len(self.comp)
        x_l2 = len(comp2.comp[0])
        y_l2 = len(comp2.comp)
        if (self._y > comp2._y + y_l2) or (self._y <= comp2._y + y_l2 and self._y + y_l1 < comp2._y):
            return False
        if (self._x > comp2._x + x_l2) or (self._x <= comp2._x + x_l2 and self._x + x_l1 < comp2._x):
            return False
        return True
    
    def move_component(self, moved_x, moved_y):     
        if moved_x <= LEFT_OFFSET or moved_x >= (WIDTH - 1):
            self._vel_x *= -1
        elif moved_y <= TOP_OFFSET:
            self._vel_y *= -1
        elif moved_y >= (HEIGHT - 1):
           #self.__do_display = False
           self._vel_y *= -1 
        else:
            self._x = moved_x
            self._y = moved_y

    
    def display_component(self):
        for i in range(len(self.comp)):
            for j in range(len(self.comp[i])):
                if self._color == "GREEN":
                    self.game_arena.arena[self._y + i][self._x + j] = Fore.RED + Back.GREEN + self.comp[i][j] + Style.RESET_ALL
                elif self._color == "YELLOW":
                    self.game_arena.arena[self._y + i][self._x + j] = Fore.RED + Back.YELLOW + self.comp[i][j] + Style.RESET_ALL
                elif self._color == "MAGENTA":
                    self.game_arena.arena[self._y + i][self._x + j] = Fore.RED + Back.CYAN + self.comp[i][j] + Style.RESET_ALL
                else:
                    self.game_arena.arena[self._y + i][self._x + j] = Fore.WHITE + Back.BLACK + self.comp[i][j] + Style.RESET_ALL
        
