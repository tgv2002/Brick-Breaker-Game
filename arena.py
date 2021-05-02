from heads import *

def display_time(time_passed):
    secs = floor(time_passed)
    if secs < 60:
        return (str(time_passed) + "s")
    elif secs < 3600:
        mins = secs // 60
        time_passed -= (mins * 60)
        return (str(mins) + "m " + str(time_passed) + "s")
    else:
        hours = secs // 3600
        mins = (secs % 3600) // 60
        time_passed -= ((mins * 60) + (hours * 3600))
        return (str(hours) + "h " + str(mins) + "m " + str(time_passed) + "s")

class Arena:   
    def __init__(self, height, width):
        self.arena = []
        self.__height = height
        self.__width = width
        
    def display_arena(self):
        for h in range(self.__height):
            for w in range(self.__width):
                print(self.arena[h][w], end = '')
            print()
            
    def refresh_arena(self, TIME, SCORE, LIVES, LEVEL, display_shooting_paddle_timer, SHOOTING_PADDLE_TIME_LEFT, boss_enemy_health_bar):
        titl = Fore.YELLOW + "BRICK-BREAKER" + "                                  " + boss_enemy_health_bar + Style.RESET_ALL
        details = Fore.RED + "Score: " + str(SCORE) + "                         " + "Lives Remaining: " + str(LIVES) + "                         " + "Level: " + str(LEVEL) + "                         "+ "Time elapsed: " + display_time(TIME) + Style.RESET_ALL
        sp_timer = Fore.GREEN +  "Time remaining for shooting paddle power up: " + display_time(SHOOTING_PADDLE_TIME_LEFT) + Style.RESET_ALL        
        leng_titl = len(titl)
        leng_details = len(details)
        sp_leng = len(sp_timer)
        ctr_titl = 0
        ctr_details = 0
        ctr_sp = 0
            
        for h in range(TOP_OFFSET):
            for w in range(self.__width + LEFT_OFFSET):
                if w < LEFT_OFFSET:
                    self.arena[h][w] = ' '
                elif h == 0:
                    self.arena[h][w] = '-'
                elif h != 2 and h != 4 and (w == LEFT_OFFSET or w == (self.__width - 1)):
                    self.arena[h][w] = '|'
                else:
                    if h == 2:
                        if w < 93:
                            self.arena[h][w] = ' '
                        elif w >= (93 + leng_titl):
                            self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = titl[ctr_titl]
                            ctr_titl += 1
                    elif h == 4:
                        if w < 36:
                            self.arena[h][w] = ' '
                        elif w >= (36 + leng_details):
                            self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = details[ctr_details]
                            ctr_details += 1
                    else:
                        self.arena[h][w] = ' '
            
        for h in range(TOP_OFFSET, self.__height):
            for w in range(self.__width + LEFT_OFFSET):
                if h == 48:
                    if w < 80:
                        self.arena[h][w] = ' '
                    elif w >= (80 + sp_leng):
                        self.arena[h][w] = ' '
                    elif display_shooting_paddle_timer:
                        self.arena[h][w] = sp_timer[ctr_sp]
                        ctr_sp += 1
                    else:
                        self.arena[h][w] = ' '  
                elif w < LEFT_OFFSET:
                    self.arena[h][w] = ' '
                elif h == 0 or h == (self.__height - 1) or h == TOP_OFFSET:
                    self.arena[h][w] = '-'
                elif w == LEFT_OFFSET or w == (self.__width - 1):
                    self.arena[h][w] = '|'
                else:
                    self.arena[h][w] = ' '
    
    def game_over_arena(self, SCORE, did_win): 
        over = []
        over.append(Fore.YELLOW + " _______  _______  _______  _______    _______           _______  _______ " + Style.RESET_ALL)
        over.append(Fore.YELLOW + "(  ____ \(  ___  )(       )(  ____ \  (  ___  )|\     /|(  ____ \(  ____ )" + Style.RESET_ALL)
        over.append(Fore.YELLOW + "| (    \/| (   ) || () () || (    \/  | (   ) || )   ( || (    \/| (    )|" + Style.RESET_ALL)
        over.append(Fore.YELLOW + "| |      | (___) || || || || (__      | |   | || |   | || (__    | (____)|" + Style.RESET_ALL)
        over.append(Fore.YELLOW + "| | ____ |  ___  || |(_)| ||  __)     | |   | |( (   ) )|  __)   |     __)" + Style.RESET_ALL)
        over.append(Fore.YELLOW + "| | \_  )| (   ) || |   | || (        | |   | | \ \_/ / | (      | (\ (   " + Style.RESET_ALL)
        over.append(Fore.YELLOW + "| (___) || )   ( || )   ( || (____/\  | (___) |  \   /  | (____/\| ) \ \__" + Style.RESET_ALL)
        over.append(Fore.YELLOW + "(_______)|/     \||/     \|(_______/  (_______)   \_/   (_______/|/   \__/" + Style.RESET_ALL)
                                                                          
        sc = Fore.GREEN + "You WON!!!!!!!!!!!!!!!" + Style.RESET_ALL
        if not did_win:
            sc = Fore.RED + "You LOST!!!!!!!!!!!!!" + Style.RESET_ALL
        high_sc = Fore.CYAN + "Your Score is: " + str(SCORE) + Style.RESET_ALL
        quitt = Fore.WHITE + "Press 'q' to exit " + Style.RESET_ALL
        again = Fore.WHITE + "Press 's' to play again " + Style.RESET_ALL
        leng_over = len(over[0])
        leng_sc = len(sc)
        leng_high_sc =len(high_sc)
        leng_quitt = len(quitt)
        leng_again = len(again)
        ctr_over = [0, 0, 0, 0, 0, 0, 0, 0]
        ctr_sc = 0
        ctr_high_sc = 0
        ctr_quitt = 0
        ctr_again = 0
            
        for h in range(self.__height):
            for w in range(self.__width + LEFT_OFFSET):
                if w < LEFT_OFFSET:
                    self.arena[h][w] = ' '
                elif h == 0  or h == (self.__height - 1):
                    self.arena[h][w] = '-'
                elif ((h < 6 or h > 13) and h != 20 and h != 22 and h != 31 and h != 33) and (w == LEFT_OFFSET or w == (self.__width - 1)):
                    self.arena[h][w] = '|'
                else:
                    if h >= 6 and h <= 13:
                        if w < 65:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = '|'
                        elif w >= (65 + leng_over):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = over[h-6][ctr_over[h-6]]
                            ctr_over[h-6] += 1
                    elif h == 20:
                        if w < 85:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (85 + leng_sc):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = sc[ctr_sc]
                            ctr_sc += 1
                    elif h == 22:
                        if w < 85:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (85 + leng_high_sc):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = high_sc[ctr_high_sc]
                            ctr_high_sc += 1                       
                    elif h == 31:
                        if w < 85:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (85 + leng_quitt):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = quitt[ctr_quitt]
                            ctr_quitt += 1 
                    elif h == 33:
                        if w < 85:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (85 + leng_again):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = again[ctr_again]
                            ctr_again += 1                       
                    else:
                        self.arena[h][w] = ' '      
    
    def intro_screen(self):
        over = []
        over.append(Fore.YELLOW + " ______   _______     _____   ______  ___  ____    ______   _______     ________       _       ___  ____   ________  _______     " + Style.RESET_ALL)
        over.append(Fore.YELLOW + "|_   _ \ |_   __ \   |_   _|.' ___  ||_  ||_  _|  |_   _ \ |_   __ \   |_   __  |     / \     |_  ||_  _| |_   __  ||_   __ \    "  + Style.RESET_ALL)
        over.append(Fore.YELLOW + "  | |_) |  | |__) |    | | / .'   \_|  | |_/ /      | |_) |  | |__) |    | |_ \_|    / _ \      | |_/ /     | |_ \_|  | |__) |   " + Style.RESET_ALL)
        over.append(Fore.YELLOW + "  |  __'.  |  __ /     | | | |         |  __'.      |  __'.  |  __ /     |  _| _    / ___ \     |  __'.     |  _| _   |  __ /    " + Style.RESET_ALL)
        over.append(Fore.YELLOW + " _| |__) |_| |  \ \_  _| |_\ `.___.'\ _| |  \ \_   _| |__) |_| |  \ \_  _| |__/ | _/ /   \ \_  _| |  \ \_  _| |__/ | _| |  \ \_  " + Style.RESET_ALL)
        over.append(Fore.YELLOW + "|_______/|____| |___||_____|`.____ .'|____||____| |_______/|____| |___||________||____| |____||____||____||________||____| |___| " + Style.RESET_ALL) 
            
        sc = Fore.RED + "Here are the brief set of instructions to keep in mind: " + Style.RESET_ALL
        rule_1 = Fore.CYAN + "1) There are 12 lives in total. There are 3 levels, each harder than the previous one. " + Style.RESET_ALL
        rule_2 = Fore.CYAN + "2) In first 2 levels, destroy all the bricks with the ball, with the help of powerups and paddle." + Style.RESET_ALL
        rule_3 = Fore.CYAN + "3) In the final level, decrease boss enemy's health to 0 with the power of the ball and paddle and win the game!" + Style.RESET_ALL
        rule_4 = Fore.CYAN + "4) Press 'a' to move paddle one unit to the left" + Style.RESET_ALL
        rule_5 = Fore.CYAN + "5) Press 'd' to move paddle one unit to the right" + Style.RESET_ALL
        rule_6 = Fore.CYAN + "6) Press 'l' to release the ball from the paddle (even in case of powerups)" + Style.RESET_ALL
        rule_7 = Fore.CYAN + "7) Press 'n' key to skip directly to the next level. Game ends when this is pressed in the last level." + Style.RESET_ALL
        
        quitt = Fore.WHITE + "Press 's' to get started! " + Style.RESET_ALL
        leng_over = len(over[0])
        leng_sc = len(sc)
        leng_rule_1 = len(rule_1)
        leng_rule_2 = len(rule_2)
        leng_rule_3 = len(rule_3)
        leng_rule_4 = len(rule_4)
        leng_rule_5 = len(rule_5)
        leng_rule_6 = len(rule_6)
        leng_rule_7 = len(rule_7)

        leng_quitt = len(quitt)
        ctr_over = [0, 0, 0, 0, 0, 0]
        ctr_sc = 0
        ctr_rule_1 = 0
        ctr_rule_2 = 0
        ctr_rule_3 = 0
        ctr_rule_4 = 0
        ctr_rule_5 = 0
        ctr_rule_6 = 0
        ctr_rule_7 = 0

        ctr_quitt = 0
            
        for h in range(self.__height):
            for w in range(self.__width + LEFT_OFFSET):
                if w < LEFT_OFFSET:
                    self.arena[h][w] = ' '
                elif h == 0 or h == (self.__height - 1):
                    self.arena[h][w] = '-'
                elif ((h < 7 or h > 12) and (not (h >= 20 and h <= 36 and h % 2 == 0)) and h != 40) and (w == LEFT_OFFSET or w == (self.__width - 1)):
                    self.arena[h][w] = '|'
                else:
                    if h >= 7 and h <= 12:
                        if w < 37:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (37 + leng_over):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = over[h-7][ctr_over[h-7]]
                            ctr_over[h-7] += 1
                    elif h == 20:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_sc):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = sc[ctr_sc]
                            ctr_sc += 1
                    elif h == 22:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_1):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_1[ctr_rule_1]
                            ctr_rule_1 += 1  
                    elif h == 24:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_2):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_2[ctr_rule_2]
                            ctr_rule_2 += 1
                    elif h == 26:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_3):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_3[ctr_rule_3]
                            ctr_rule_3 += 1
                    elif h == 28:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_4):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_4[ctr_rule_4]
                            ctr_rule_4 += 1   
                    elif h == 30:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_5):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_5[ctr_rule_5]
                            ctr_rule_5 += 1   
                    elif h == 32:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_6):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_6[ctr_rule_6]
                            ctr_rule_6 += 1       
                    elif h == 34:
                        if w < 50:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (50 + leng_rule_7):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = rule_7[ctr_rule_7]
                            ctr_rule_7 += 1                                    
                    elif h == 40:
                        if w < 85:
                            if w != LEFT_OFFSET:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        elif w >= (85 + leng_quitt):
                            if w != self.__width - 1:
                                self.arena[h][w] = ' '
                            else:
                                self.arena[h][w] = ' '
                        else:
                            self.arena[h][w] = quitt[ctr_quitt]
                            ctr_quitt += 1                        
                    else:
                        self.arena[h][w] = ' '       
             
    def setup_arena(self, TIME, SCORE, LIVES, LEVEL, display_shooting_paddle_timer, SHOOTING_PADDLE_TIME_LEFT):
        titl = Fore.YELLOW + "BRICK-BREAKER" + Style.RESET_ALL
        details = Fore.RED + "Score: " + str(SCORE) + "                         " + "Lives Remaining: " + str(LIVES) + "                         " + "Level: " + str(LEVEL) + "                         "+ "Time elapsed: " + display_time(TIME) + Style.RESET_ALL
        leng_titl = len(titl)
        leng_details = len(details)
        ctr_titl = 0
        ctr_details = 0
            
        for h in range(TOP_OFFSET):
            self.head_arr = []
            for w in range(self.__width + LEFT_OFFSET):
                if w < LEFT_OFFSET:
                    self.head_arr.append(' ')
                elif h == 0:
                    self.head_arr.append('-')
                elif h != 2 and h != 4 and (w == LEFT_OFFSET or w == (self.__width - 1)):
                    self.head_arr.append('|')
                else:
                    if h == 2:
                        if w < 93:
                            self.head_arr.append(' ')
                        elif w >= (93 + leng_titl):
                            self.head_arr.append(' ')
                        else:
                            self.head_arr.append(titl[ctr_titl])
                            ctr_titl += 1
                    elif h == 4:
                        if w < 36:
                            self.head_arr.append(' ')
                        elif w >= (36 + leng_details):
                            self.head_arr.append(' ')
                        else:
                            self.head_arr.append(details[ctr_details])
                            ctr_details += 1
                    else:
                        self.head_arr.append(' ')
            self.arena.append(self.head_arr)
            
        for h in range(TOP_OFFSET, self.__height):
            self.empty_arr = []
            for w in range(self.__width + LEFT_OFFSET):
                if w < LEFT_OFFSET:
                    self.empty_arr.append(' ')
                elif h == 0 or h == (self.__height - 1) or h == TOP_OFFSET:
                    self.empty_arr.append('-')
                elif w == LEFT_OFFSET or w == (self.__width - 1):
                    self.empty_arr.append('|')
                else:
                    self.empty_arr.append(' ')
            self.arena.append(self.empty_arr)