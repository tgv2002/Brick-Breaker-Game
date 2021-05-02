from heads import *
from component import *
from helper import *
from ball import *

class BossEnemy(Component):
    def __init__(self, x, y, color, vel_x, vel_y, game_arena, health):
        super().__init__(x, y, color, vel_x, vel_y, game_arena)
        self.__do_display = False
        self.__health = health
        self.__health_bar = "|" * health
        self.__num_times_spawn_bricks_below = 2
        self.__currently_existing_spawned_bricks = 0

        
    def display_component(self):                        
        if self.__do_display:
            for i in range(len(self.comp)):
                for j in range(len(self.comp[i])):
                    self.game_arena.arena[self._y + i][self._x + j] = Fore.YELLOW + self.comp[i][j] + Style.RESET_ALL
    
    def create_boss_enemy(self):
        self.comp.append("                _____                ")
        self.comp.append('             ,-"     "-.             ')
        self.comp.append("            / o       o \            ")
        self.comp.append("           /   \     /   \           ")
        self.comp.append('          /     )-"-(     \          ')
        self.comp.append('         /     ( 6 6 )     \         ') 
        self.comp.append('        /       \ " /       \        ')
        self.comp.append('       /         )=(         \       ')
        self.comp.append('      /   o   .--"-"--.   o   \      ')
        self.comp.append('     /    I  /  -   -  \  I    \     ') 
        self.comp.append(' .--(    (_}y/\       /\y{_)    )--. ') 
        self.comp.append('(    ".___l\/__\_____/__\/l___,"    )')
        self.comp.append(' \                                 / ')
        self.comp.append('  "-._      o O o O o O o      _,-"  ')
        self.comp.append("      `--Y--.___________.--Y--'      ")
        self.comp.append("         |==.___________.==|         ") 
        self.comp.append("         '==.___________.=='         ") 

    def get_health(self):
        return self.__health
    
    def get_health_bar(self):
        return self.__health_bar
    
    def set_health_bar(self, hb):
        self.__health_bar = hb

    def set_health(self, strengthVal):
        self.__health = strengthVal
        self.__health_bar = "|" * strengthVal 
        
    def can_display_boss_enemy(self):
        return self.__do_display
    
    def set_display_status(self, statusVal):
        self.__do_display = statusVal
        
    def get_num_times_spawn_bricks_below(self):
        return self.__num_times_spawn_bricks_below
    
    def set_num_times_spawn_bricks_below(self, num_times):
        self.__num_times_spawn_bricks_below = num_times
        
    def get_currently_existing_spawned_bricks(self):
        return self.__currently_existing_spawned_bricks
    
    def set_currently_existing_spawned_bricks(self, num_times):
        self.__currently_existing_spawned_bricks = num_times
        
    def got_hit(self):
        self.__health -= 1
        self.__health_bar = "|" * self.__health
        if self.__health == 0:
            self.__do_display = False
        return 20
            
    def move_component(self, moved_x):
        if moved_x <= LEFT_OFFSET:
            self._x = LEFT_OFFSET + 1 
        elif moved_x >= (WIDTH - 38):
            self._x = WIDTH - 38
        else:
            self._x = moved_x  
            
    