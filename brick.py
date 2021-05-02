from heads import *
from component import *
from helper import *
from ball import *

class Brick(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena, strength, is_unbreakable, is_explosive, will_explode, is_rainbow):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__strength = strength
        self.__do_display = True
        self.__unbreakable = is_unbreakable
        self.__is_explosive = is_explosive
        self.__is_rainbow = is_rainbow
        self.__will_explode = will_explode
        
    def display_component(self):                        
        if self.__do_display:
            for i in range(len(self.comp)):
                for j in range(len(self.comp[i])):
                    if self._color == "GREEN":
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.GREEN + Back.GREEN + self.comp[i][j] + Style.RESET_ALL
                    elif self._color == "YELLOW":
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.YELLOW + Back.YELLOW + self.comp[i][j] + Style.RESET_ALL
                    elif self._color == "BLUE":
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.BLUE + Back.BLUE + self.comp[i][j] + Style.RESET_ALL
                    elif self._color == "RED":
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.RED + Back.RED + self.comp[i][j] + Style.RESET_ALL
                    else:
                        self.game_arena.arena[self._y + i][self._x + j] = Fore.RED + Back.YELLOW + self.comp[i][j] + Style.RESET_ALL
                
    def create_brick(self):
        self.comp.append("         ")
    
    def create_exploding_brick(self):
        self.comp.append("|  TNT  |")
    
    def is_rainbow(self):
        return self.__is_rainbow
    
    def set_rainbow_status(self, is_rainbow):
        self.__is_rainbow = is_rainbow
        
    def is_explosive(self):
        return self.__is_explosive
    
    def will_explode(self):
        return self.__will_explode
    
    def get_strength(self):
        return self.__strength

    def set_strength(self, strengthVal):
        self.__strength = strengthVal
        
    def can_display_brick(self):
        return self.__do_display
    
    def set_display_status(self, statusVal):
        self.__do_display = statusVal
    
    def big_blast(self, game_bricks):
        os.system('aplay -q ./sound_effects/explosion.wav&')
        for game_brick in game_bricks:
            if game_brick.can_display_brick() and game_brick.will_explode():
                game_brick.set_strength(0)
                game_brick.set_display_status(False)
        return 100
    
    def neighbour_blast(self, game_bricks):
        os.system('aplay -q ./sound_effects/explosion.wav&')
        for game_brick in game_bricks:
            if game_brick.can_display_brick():
                diff_x = game_brick.get_x() - self._x
                diff_y = game_brick.get_y() - self._y
                if (diff_x >= -15 and diff_x <= 15) and (diff_y >= -2 and diff_y <= 2):
                    game_brick.set_strength(0)
                    game_brick.set_display_status(False)
        return 35
        
    def is_unbreakable(self):
        return self.__unbreakable
        
    def got_hit(self, in_power_mode, game_bricks, in_fire_mode):
        power_rise = 5
        if self.is_explosive():
            return self.big_blast(game_bricks)
        if in_fire_mode:
            return self.neighbour_blast(game_bricks)
        if in_power_mode:
            if self.__unbreakable:
                power_rise = 25
            elif self.__strength == 2:
                power_rise = 10
            elif self.__strength == 3:
                power_rise = 15
            self.__strength = 0
            self.__do_display = False
        elif not self.__unbreakable:
            self.__strength -= 1
            if self.__strength == 0:
                self.__do_display = False
            elif self.__strength == 2:
                self.set_color("GREEN")
            elif self.__strength == 1:
                self.set_color("BLUE")
        else:
            power_rise = 0
        return power_rise
            
    