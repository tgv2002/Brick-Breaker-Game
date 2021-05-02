from heads import *
from arena import *
from ball import *
from brick import *
from paddle import *
from powerUp import *
from component import *
from paddleGrab import *
from expandPaddle import *
from shrinkPaddle import *
from thruBall import *
from fastBall import *
from ballMultiplier import *
from shootingPaddle import *
from fireBall import *
from cannon import *
from bullet import *
from boss_bomb import *
from boss_enemy import *
from input import *

game_balls = []
game_bricks = []
game_boss_enemy_unbreakable_bricks = []
game_boss_enemy_spawned_bricks = []
game_boss_bombs = []
game_paddle_grabs = []
game_expand_paddles = []
game_shrink_paddles = []
game_thru_balls = []
game_fire_balls = []
game_fast_balls = []
game_shooting_paddles = []
game_ball_multipliers = []
game_bullets = []
SCORE = 0
LEVEL = 1
LIVES = 12
TIME = 0
SHOOTING_PADDLE_TIME_LEFT = 0
display_shooting_paddle_timer = False

time_of_starting = time.time()
prev_time = 0

game_arena = Arena(HEIGHT, WIDTH)
game_boss_enemy = BossEnemy(WIDTH//2 + 4, 43, "MAGENTA", 0, 0, game_arena, 12)
game_arena.setup_arena(TIME, SCORE, LIVES, LEVEL, display_shooting_paddle_timer, SHOOTING_PADDLE_TIME_LEFT)
game_paddle = Paddle(WIDTH//2 + 4, 43, "MAGENTA", 0, 0, game_arena, 12)
game_cannon_1 = Cannon(WIDTH//2 + 4, 42, "MAGENTA", 0, 0, game_arena)
game_cannon_2 = Cannon(WIDTH//2 + 14, 42, "MAGENTA", 0, 0, game_arena)

def getScore():
    global SCORE
    return SCORE 

def getLevel():
    global LEVEL
    return LEVEL

def getLives():
    global LIVES
    return LIVES 

def updateScore(inc):
    global SCORE
    SCORE += inc

def get_boss_enemy_health_bar():
    global game_boss_enemy
    if game_boss_enemy.can_display_boss_enemy():
        return "Boss Enemy Health: " + game_boss_enemy.get_health_bar()
    return ""
    
def current_ball_count():
    global game_balls
    ball_count = 0
    for game_ball in game_balls:
        if game_ball.can_display_ball():
            ball_count += 1
    return ball_count   

def updateLives():
    global LIVES
    if current_ball_count() == 0:
        os.system('aplay -q ./sound_effects/life_lost.wav&')
        if getLevel() == 3:
            reset_boss_level()       
        LIVES -= 1
        if LIVES > 0:
            return reset_game()
        else:
            return end_game()
    return 1

def reset_boss_level():
    global game_balls
    global game_boss_enemy
    global game_boss_bombs
    game_balls.clear()
    game_boss_enemy.set_x(WIDTH//2 - 4)
    game_boss_enemy.set_y(7)
    game_boss_bombs.clear()
    paddle_ball_setup()
    return 0

def subtract_lives():
    global LIVES
    os.system('aplay -q ./sound_effects/life_lost.wav&')       
    LIVES -= 1
    if LIVES > 0:
        return reset_boss_level()
    return end_game() 

def corresponding_color(strength):
    if strength == 1:
        return "BLUE"
    if strength == 2:
        return "GREEN"
    if strength == 3:
        return "YELLOW"
    if strength == INF:
        return "RED"
    return "WHITE"

def only_unbreakable_left():
    global game_bricks
    brick_count = 0
    for i in range(len(game_bricks)):
        if game_bricks[i].can_display_brick() and not game_bricks[i].is_unbreakable():
            brick_count += 1
    return brick_count == 0
    
def all_bricks_done():
    global game_bricks
    brick_count = 0
    for i in range(len(game_bricks)):
        if game_bricks[i].can_display_brick():
            brick_count += 1
    return brick_count == 0

def did_win():
    global game_boss_enemy
    if (not all_bricks_done()) or (game_boss_enemy.can_display_boss_enemy()):
        return False
    return LIVES > 0

def setup_bricks():
    global game_bricks
    global game_arena
    ctr = -1
    for j in range(9):
        for i in range(9):
            if j < 4:
                if i < (4 - j) or i >= (5 + j):
                    continue
            elif j > 4:
                if i < (j - 4) or i >= (13 - j):
                    continue
            ctr += 1
            if j == 8 or j == 7 or (j == 6 and (i == 2 or i == 6)):
                game_bricks.append(Brick(LEFT_OFFSET + 15*(i+1), TOP_OFFSET + (2*(j+1)), corresponding_color(4), 0, 0, game_arena, 4, False, True, True, False))
                game_bricks[ctr].create_exploding_brick()
            else:
                if not ((j == 3 and i == 4) or (j == 4 and (i == 3 or i == 4 or i == 5)) or (j == 5 and i == 4)):
                    game_bricks.append(Brick(LEFT_OFFSET + 15*(i+1), TOP_OFFSET + (2*(j+1)), corresponding_color(1 + (ctr % 3)), 0, 0, game_arena, 1 + (ctr % 3), False, False, j == 6 or j == 5, (i == j) or (i + j == 8) or (j == 4)))
                else:
                    game_bricks.append(Brick(LEFT_OFFSET + 15*(i+1), TOP_OFFSET + (2*(j+1)), corresponding_color(INF), 0, 0, game_arena, INF, True, False, False, False))
                game_bricks[ctr].create_brick()     


def setup_bricks_second_level():
    global game_bricks
    global game_arena
    ctr = -1
    num = 0
    for j in range(9):
        num += 1
        for i in range(9):
            if (j == 0 or j == 8) and (i % 4 != 0):
                continue
            elif (j == 1 or j == 7) and (i % 4 == 2):
                continue
            ctr += 1
            if (j == 7 and i >= 3 and i <= 5) or (j == 8 and i == 4) or (j == 6 and (i % 4 == 2)):
                game_bricks.append(Brick(LEFT_OFFSET + 15*(i+1), TOP_OFFSET + (2*(j+1)), corresponding_color(4), 0, 0, game_arena, 4, False, True, True, False))
                game_bricks[ctr].create_exploding_brick()
            else:
                if not ((j == 3 and i == 4) or (j == 4 and (i >= 3 and i <= 5)) or (j == 5 and i == 4)):
                    rand_type = random.randint(0, 3)
                    game_bricks.append(Brick(LEFT_OFFSET + 15*(i+1), TOP_OFFSET + (2*(j+1)), corresponding_color(1 + ((ctr + num) % 3)), 0, 0, game_arena, 1 + ((num + ctr) % 3), False, False, j >= 5 and (i != 0 and i != 8), (i == j) or (i + j == 8) or (j == 4)))
                else:
                    game_bricks.append(Brick(LEFT_OFFSET + 15*(i+1), TOP_OFFSET + (2*(j+1)), corresponding_color(INF), 0, 0, game_arena, INF, True, False, False, False))
                game_bricks[ctr].create_brick()        

def shift_bricks_downwards():
    global game_bricks
    for i in range(len(game_bricks)):
        if game_bricks[i].can_display_brick():
            game_bricks[i].set_y(game_bricks[i].get_y() + 1)
            
def bricks_reached_paddle_level():
    global game_bricks
    max_y = -INF
    for i in range(len(game_bricks)):
        if game_bricks[i].can_display_brick():
            max_y = max(game_bricks[i].get_y(), max_y)
    return max_y >= 43   

def rainbow_bricks_gimmicks():
    global game_bricks
    for i in range(len(game_bricks)):
        if game_bricks[i].can_display_brick() and game_bricks[i].is_rainbow():
            game_bricks[i].set_strength((game_bricks[i].get_strength() % 3) + 1)
            game_bricks[i].set_color(corresponding_color(game_bricks[i].get_strength()))

def setup_boss_level():
    global game_boss_enemy
    global game_boss_enemy_unbreakable_bricks
    game_boss_enemy = BossEnemy(WIDTH//2 - 4, 7, "MAGENTA", 0, 0, game_arena, 12)
    game_boss_enemy.create_boss_enemy()
    game_boss_enemy.set_display_status(True)
    boss_width = 37
    boss_height = 17
    ctr = -1
    for i in range(LEFT_OFFSET + 15, WIDTH - 5, 24):
        ctr += 1
        game_boss_enemy_unbreakable_bricks.append(Brick(i, 26, corresponding_color(INF), 0, 0, game_arena, INF, True, False, False, False))
        game_boss_enemy_unbreakable_bricks[ctr].create_brick()   

def spawn_bricks(y):
    global game_boss_enemy
    global game_boss_enemy_spawned_bricks
    game_boss_enemy_spawned_bricks.clear()
    ctr = -1
    for j in range(9):
        ctr += 1
        game_boss_enemy_spawned_bricks.append(Brick(LEFT_OFFSET + 15*(j+1), y, corresponding_color(1 + (ctr % 3)), 0, 0, game_arena, 1 + (ctr % 3), False, False, False, False))
        game_boss_enemy_spawned_bricks[ctr].create_brick()
    game_boss_enemy.set_currently_existing_spawned_bricks(ctr + 1)
           
def monitor_boss_spawning_bricks():
    global game_boss_enemy
    global game_boss_enemy_spawned_bricks
    if game_boss_enemy.can_display_boss_enemy():
        curr_h = game_boss_enemy.get_health()
        if game_boss_enemy.get_num_times_spawn_bricks_below() == 2:
            if curr_h == 5:
                game_boss_enemy.set_num_times_spawn_bricks_below(1)
                os.system('aplay -q ./sound_effects/bullet_shot.wav&')
                spawn_bricks(29)
        elif game_boss_enemy.get_num_times_spawn_bricks_below() == 1:
            if len(game_boss_enemy_spawned_bricks) <= 3:
                game_boss_enemy.set_num_times_spawn_bricks_below(0)
                os.system('aplay -q ./sound_effects/bullet_shot.wav&')
                spawn_bricks(31)    
                  
def paddle_ball_setup():
    global game_paddle
    global game_cannon_1
    global game_cannon_2
    global game_balls
    global game_arena
    
    game_paddle = Paddle(WIDTH//2 + 4, 43, "MAGENTA", 0, 0, game_arena, 12)
    game_cannon_1 = Cannon(WIDTH//2 + 4, 42, "MAGENTA", 0, 0, game_arena)
    game_cannon_2 = Cannon(WIDTH//2 + 14, 42, "MAGENTA", 0, 0, game_arena)
    game_cannon_1.create_cannon()
    game_cannon_2.create_cannon()
    game_paddle.create_paddle()

    game_balls.append(Ball(random.randint(WIDTH//2 + 4, WIDTH//2 + 15), 42, "YELLOW", 1, -1, game_arena))
    game_balls[0].create_ball()
    game_balls[0].update_movement_status(True)
    
def remove_power_ups_effect():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global game_arena
    global game_bullets
    global game_boss_bombs
    global SHOOTING_PADDLE_TIME_LEFT
    global display_shooting_paddle_timer
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.is_active():
            game_paddle_grab.remove_paddle_grab(game_paddle)
    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.is_active():
            game_expand_paddle.remove_expand_paddle(game_paddle)
    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.is_active():
            game_shrink_paddle.remove_shrink_paddle(game_paddle)
    for game_thru_ball in game_thru_balls:
        if game_thru_ball.is_active():
            game_thru_ball.remove_power_ball(game_balls)
    for game_fire_ball in game_fire_balls:
        if game_fire_ball.is_active():
            game_fire_ball.remove_fire_ball(game_balls)
    for game_fast_ball in game_fast_balls:
        if game_fast_ball.is_active():
            game_fast_ball.remove_fasten_ball(game_balls)
    game_bullets.clear()
    game_boss_bombs.clear()
    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.is_active():
            game_shooting_paddle.remove_shooting_paddle()
    display_shooting_paddle_timer = False
    SHOOTING_PADDLE_TIME_LEFT = 0
    

def reset_game():
    global game_balls
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global SHOOTING_PADDLE_TIME_LEFT
    global display_shooting_paddle_timer
    
    remove_power_ups_effect()
    game_balls.clear()
    game_paddle_grabs.clear()
    game_expand_paddles.clear()
    game_shooting_paddles.clear()
    game_shrink_paddles.clear()
    game_thru_balls.clear()
    game_fire_balls.clear()
    game_fast_balls.clear()
    game_ball_multipliers.clear()
    display_shooting_paddle_timer = False
    SHOOTING_PADDLE_TIME_LEFT = 0
    
    paddle_ball_setup()
    return 0

def setup_game():
    global game_balls
    global game_bricks
    global game_boss_enemy_spawned_bricks
    global game_boss_enemy_unbreakable_bricks
    global game_boss_enemy
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global SCORE
    global LIVES
    global LEVEL
    global TIME
    global time_of_starting
    global prev_time
    global SHOOTING_PADDLE_TIME_LEFT
    global display_shooting_paddle_timer
    
    remove_power_ups_effect()
    game_balls.clear()
    game_bricks.clear()
    game_boss_enemy_spawned_bricks.clear()
    game_boss_enemy_unbreakable_bricks.clear()
    game_paddle_grabs.clear()
    game_expand_paddles.clear()
    game_shrink_paddles.clear()
    game_thru_balls.clear()
    game_fire_balls.clear()
    game_fast_balls.clear()
    game_boss_enemy.set_display_status(False)
    game_shooting_paddles.clear()
    game_ball_multipliers.clear()
    
    setup_bricks()
    paddle_ball_setup()
    SCORE = 0
    LIVES = 12
    LEVEL = 1
    TIME = 0
    display_shooting_paddle_timer = False
    SHOOTING_PADDLE_TIME_LEFT = 0
    time_of_starting = time.time()
    prev_time = 0      

def manage_display():
    print('\033[0;0H')

def paddle_powerup_check():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global game_arena
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.can_display_power_up() and game_paddle.collided(game_paddle_grab):
            game_paddle_grab.paddle_grab(game_paddle)
    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.can_display_power_up() and game_paddle.collided(game_expand_paddle):
            game_expand_paddle.expand_paddle(game_paddle)
    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.can_display_power_up() and game_paddle.collided(game_shrink_paddle):
            game_shrink_paddle.shrink_paddle(game_paddle)
    for game_thru_ball in game_thru_balls:
        if game_thru_ball.can_display_power_up() and game_paddle.collided(game_thru_ball):
            game_thru_ball.power_ball(game_balls)
    for game_fire_ball in game_fire_balls:
        if game_fire_ball.can_display_power_up() and game_paddle.collided(game_fire_ball):
            game_fire_ball.fire_ball(game_balls)
    for game_fast_ball in game_fast_balls:
        if game_fast_ball.can_display_power_up() and game_paddle.collided(game_fast_ball):
            game_fast_ball.fasten_ball(game_balls)
    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.can_display_power_up() and game_paddle.collided(game_shooting_paddle):
            game_shooting_paddle.shoot_from_paddle()
    for game_ball_multiplier in game_ball_multipliers:
        if game_ball_multiplier.can_display_power_up() and game_paddle.collided(game_ball_multiplier):
            new_game_balls = []
            for game_ball in game_balls:
                if game_ball.can_display_ball():
                    v_x, v_y = game_ball_multiplier.multiply_ball(game_ball)
                    new_game_balls.append(Ball(game_ball.get_x(), game_ball.get_y(), "YELLOW", v_x, v_y, game_arena))
            for new_ball in new_game_balls:
                game_balls.append(new_ball)
                game_balls[len(game_balls)-1].create_ball()
                game_balls[len(game_balls)-1].update_movement_status(False)

def powerup_gravity_effect():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.can_display_power_up():
            game_paddle_grab.set_vel_y(game_paddle_grab.get_vel_y() + POWERUP_GRAVITY)
    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.can_display_power_up():
            game_expand_paddle.set_vel_y(game_expand_paddle.get_vel_y() + POWERUP_GRAVITY)
    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.can_display_power_up():
            game_shrink_paddle.set_vel_y(game_shrink_paddle.get_vel_y() + POWERUP_GRAVITY)
    for game_thru_ball in game_thru_balls:
        if game_thru_ball.can_display_power_up():
            game_thru_ball.set_vel_y(game_thru_ball.get_vel_y() + POWERUP_GRAVITY)
    for game_fire_ball in game_fire_balls:
        if game_fire_ball.can_display_power_up():
            game_fire_ball.set_vel_y(game_fire_ball.get_vel_y() + POWERUP_GRAVITY)
    for game_fast_ball in game_fast_balls:
        if game_fast_ball.can_display_power_up():
            game_fast_ball.set_vel_y(game_fast_ball.get_vel_y() + POWERUP_GRAVITY)
    for game_ball_multiplier in game_ball_multipliers:
        if game_ball_multiplier.can_display_power_up():
            game_ball_multiplier.set_vel_y(game_ball_multiplier.get_vel_y() + POWERUP_GRAVITY)
    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.can_display_power_up():
            game_shooting_paddle.set_vel_y(game_shooting_paddle.get_vel_y() + POWERUP_GRAVITY)
                                    
def displace_powerups():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.can_display_power_up():
            hit_paddle = game_paddle_grab.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_paddle_grab.paddle_grab(game_paddle)

            
                
    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.can_display_power_up():
            hit_paddle = game_expand_paddle.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_expand_paddle.expand_paddle(game_paddle)
       

    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.can_display_power_up():
            hit_paddle = game_shrink_paddle.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_shrink_paddle.shrink_paddle(game_paddle)

                
    for game_thru_ball in game_thru_balls:
        if game_thru_ball.can_display_power_up():
            hit_paddle = game_thru_ball.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_thru_ball.power_ball(game_balls)

    for game_fire_ball in game_fire_balls:
        if game_fire_ball.can_display_power_up():
            hit_paddle = game_fire_ball.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_fire_ball.fire_ball(game_balls)


    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.can_display_power_up():
            hit_paddle = game_shooting_paddle.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_shooting_paddle.shoot_from_paddle()

     
    for game_fast_ball in game_fast_balls:
        if game_fast_ball.can_display_power_up():
            hit_paddle = game_fast_ball.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                game_fast_ball.fasten_ball(game_balls)


    for game_ball_multiplier in game_ball_multipliers:
        if game_ball_multiplier.can_display_power_up():
            hit_paddle = game_ball_multiplier.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/collected_powerup.wav&')
                new_game_balls = []
                for game_ball in game_balls:
                    if game_ball.can_display_ball():
                        v_x, v_y = game_ball_multiplier.multiply_ball(game_ball)
                        new_game_balls.append(Ball(game_ball.get_x(), game_ball.get_y(), "YELLOW", v_x, v_y, game_arena))
                for new_ball in new_game_balls:
                    game_balls.append(new_ball)
                    game_balls[len(game_balls)-1].create_ball()
                    game_balls[len(game_balls)-1].update_movement_status(False)

                      
# def no_shooting_paddle_active():
#     for game_shooting_paddle in game_shooting_paddles:
#         if game_shooting_paddle.is_active():
#             return False
#     return True

def drop_bombs():
    global game_boss_enemy
    global game_boss_bombs
    if game_boss_enemy.can_display_boss_enemy() and game_boss_enemy.get_health() > 0:
        os.system('aplay -q ./sound_effects/bullet_shot.wav&')
        game_boss_bombs.append(BossBomb(game_boss_enemy.get_x() + 18, 25, "RED", 0, BOMB_DROP_VELOCITY, game_arena))
        game_boss_bombs[len(game_boss_bombs) - 1].create_bomb()
        
def move_bombs():
    global game_boss_bombs
    global game_paddle
    for game_boss_bomb in game_boss_bombs:
        if game_boss_bomb.can_display_bomb():
            hit_paddle = game_boss_bomb.move_component(game_paddle)
            if hit_paddle:
                os.system('aplay -q ./sound_effects/explosion.wav&')
                return subtract_lives()
    return 0

def get_bombs():
    global game_boss_bombs
    for game_boss_bomb in game_boss_bombs:
        if game_boss_bomb.can_display_bomb():
            game_boss_bomb.display_component()  
    

def generate_power_up(curr_brick, vx, vy):
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global game_arena
    global display_shooting_paddle_timer
    
    power_up_type = random.randint(0, 8)

    if power_up_type == 0:
        game_paddle_grabs.append(PaddleGrab(curr_brick.get_x(), curr_brick.get_y(), "GREEN", vx, vy, game_arena))
        game_paddle_grabs[len(game_paddle_grabs)-1].create_paddle_grab_power_up()
    elif power_up_type == 1:
        game_expand_paddles.append(ExpandPaddle(curr_brick.get_x(), curr_brick.get_y(), "YELLOW", vx, vy, game_arena))
        game_expand_paddles[len(game_expand_paddles)-1].create_expand_paddle_power_up()
    elif power_up_type == 2:
        game_shrink_paddles.append(ShrinkPaddle(curr_brick.get_x(), curr_brick.get_y(), "GREEN", vx, vy, game_arena))
        game_shrink_paddles[len(game_shrink_paddles)-1].create_shrink_paddle_power_up()
    elif power_up_type == 3:
        game_thru_balls.append(ThruBall(curr_brick.get_x(), curr_brick.get_y(), "YELLOW", vx, vy, game_arena))
        game_thru_balls[len(game_thru_balls)-1].create_thru_ball_power_up()
    elif power_up_type == 4:
        game_fast_balls.append(FastBall(curr_brick.get_x(), curr_brick.get_y(), "GREEN", vx, vy, game_arena))
        game_fast_balls[len(game_fast_balls)-1].create_fast_ball_power_up()
    elif power_up_type == 5:
        game_shooting_paddles.append(ShootingPaddle(curr_brick.get_x(), curr_brick.get_y(), "GREEN", vx, vy, game_arena))
        game_shooting_paddles[len(game_shooting_paddles)-1].create_shooting_paddle_power_up()
    elif power_up_type == 6:
        game_fire_balls.append(FireBall(curr_brick.get_x(), curr_brick.get_y(), "GREEN", vx, vy, game_arena))
        game_fire_balls[len(game_fire_balls)-1].create_fire_ball_power_up()     
    else:
        game_ball_multipliers.append(BallMultiplier(curr_brick.get_x(), curr_brick.get_y(), "YELLOW", vx, vy, game_arena))
        game_ball_multipliers[len(game_ball_multipliers)-1].create_ball_multiplier_power_up()


def update_power_ups_status():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global game_arena
    global game_bullets
    global game_cannon_1
    global game_cannon_2
    global display_shooting_paddle_timer
    global SHOOTING_PADDLE_TIME_LEFT
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.is_active():
            if game_paddle_grab.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_paddle_grab.remove_paddle_grab(game_paddle)
            else:
                game_paddle_grab.set_elapsed_time(game_paddle_grab.get_elapsed_time() + 1)

    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.is_active():
            if game_expand_paddle.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_expand_paddle.remove_expand_paddle(game_paddle)
            else:
                game_expand_paddle.set_elapsed_time(game_expand_paddle.get_elapsed_time() + 1)
    
    min_elapsed_time = POWERUP_TIMELIMIT                
    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.is_active():
            game_shooting_paddle.set_elapsed_time(game_shooting_paddle.get_elapsed_time() + 1)
            min_elapsed_time = min(min_elapsed_time, game_shooting_paddle.get_elapsed_time())
            if game_shooting_paddle.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_shooting_paddle.remove_shooting_paddle()
            else:
                os.system('aplay -q ./sound_effects/bullet_shot.wav&')
                vx, vy = game_cannon_1.shoot_bullet()
                game_bullets.append(Bullet(game_cannon_1.get_x(), game_cannon_1.get_y(), "RED", vx, vy, game_arena))
                game_bullets[len(game_bullets) - 1].create_bullet()
                os.system('aplay -q ./sound_effects/bullet_shot.wav&')
                vx2, vy2 = game_cannon_2.shoot_bullet()
                game_bullets.append(Bullet(game_cannon_2.get_x(), game_cannon_2.get_y(), "RED", vx2, vy2, game_arena))
                game_bullets[len(game_bullets) - 1].create_bullet()


    if min_elapsed_time == POWERUP_TIMELIMIT:
        game_bullets.clear()
        display_shooting_paddle_timer = False
        SHOOTING_PADDLE_TIME_LEFT = 0
    else:
        display_shooting_paddle_timer = True
        SHOOTING_PADDLE_TIME_LEFT = POWERUP_TIMELIMIT - min_elapsed_time

    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.is_active():
            if game_shrink_paddle.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_shrink_paddle.remove_shrink_paddle(game_paddle)
            else:
                game_shrink_paddle.set_elapsed_time(game_shrink_paddle.get_elapsed_time() + 1)

    for game_thru_ball in game_thru_balls:
        if game_thru_ball.is_active():
            if game_thru_ball.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_thru_ball.remove_power_ball(game_balls)
            else:
                game_thru_ball.set_elapsed_time(game_thru_ball.get_elapsed_time() + 1)
                
    for game_fire_ball in game_fire_balls:
        if game_fire_ball.is_active():
            if game_fire_ball.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_fire_ball.remove_fire_ball(game_balls)
            else:
                game_fire_ball.set_elapsed_time(game_fire_ball.get_elapsed_time() + 1)

    for game_fast_ball in game_fast_balls:
        if game_fast_ball.is_active():
            if game_fast_ball.get_elapsed_time() == POWERUP_TIMELIMIT - 1:
                game_fast_ball.remove_fasten_ball(game_balls)
            else:
                game_fast_ball.set_elapsed_time(game_fast_ball.get_elapsed_time() + 1)


def boss_level_collision_check(curr_point, game_ball, prev_x, prev_y):
    global game_boss_enemy
    global game_boss_enemy_spawned_bricks
    global game_boss_enemy_unbreakable_bricks
    shouldProceed = 1
    for i in range(len(game_boss_enemy_spawned_bricks)):
        if game_boss_enemy_spawned_bricks[i].can_display_brick():
            if game_boss_enemy_spawned_bricks[i].collided(game_ball):
                os.system('aplay -q ./sound_effects/ball_hit_obstacle.wav&')
                shouldProceed = 0
                rise = game_boss_enemy_spawned_bricks[i].got_hit(False, game_boss_enemy_spawned_bricks, False)
                updateScore(rise)
                if game_boss_enemy_spawned_bricks[i].get_strength() == 0:
                    game_boss_enemy.set_currently_existing_spawned_bricks(game_boss_enemy.get_currently_existing_spawned_bricks() - 1)
                game_ball.ball_reflection(game_boss_enemy_spawned_bricks[i], prev_x, prev_y)
    for i in range(len(game_boss_enemy_unbreakable_bricks)):
        if game_boss_enemy_unbreakable_bricks[i].can_display_brick():
            if game_boss_enemy_unbreakable_bricks[i].collided(game_ball):
                os.system('aplay -q ./sound_effects/ball_hit_obstacle.wav&')
                shouldProceed = 0
                game_ball.ball_reflection(game_boss_enemy_unbreakable_bricks[i], prev_x, prev_y)
    if game_boss_enemy.can_display_boss_enemy():
        if game_boss_enemy.collided(game_ball):
            os.system('aplay -q ./sound_effects/ball_hit_obstacle.wav&')
            shouldProceed = 0
            rise = game_boss_enemy.got_hit()
            updateScore(rise)
            game_ball.ball_reflection(game_boss_enemy, prev_x, prev_y)        
    return shouldProceed
    
                 
def move_ball_carefully(TIME):
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    global game_boss_enemy
    
    for game_ball in game_balls:
        if game_ball.can_display_ball() and not game_ball.get_movement_status():
            ball_vel_x = game_ball.get_vel_x()
            ball_vel_y = game_ball.get_vel_y()   
            m = INF  
            c = INF 
            
            if ball_vel_x != 0:
                m = ball_vel_y / ball_vel_x      
            x2 = game_ball.get_x() + ball_vel_x
            y2 = game_ball.get_y() + ball_vel_y        
            x1 = game_ball.get_x()
            y1 = game_ball.get_y()
            if ball_vel_x != 0:
                c = y1 - (m*x1)
            
            curr_path = []
            if ball_vel_x == 0:
                if y2 > y1:
                    for y_coord in range(y1 + 1, y2 + 1):
                        curr_path.append([x1, y_coord])
                else:
                    for y_coord in range(y1 - 1, y2 - 1, -1):
                        curr_path.append([x1, y_coord])
            else:
                if x2 > x1:
                    for x_coord in range(x1 + 1, x2 + 1):
                        if (((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1) == int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1)):
                            curr_path.append([x_coord, int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1))])
                else:
                    for x_coord in range(x1 - 1, x2 - 1, -1):
                        if (((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1) == int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1)):
                            curr_path.append([x_coord, int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1))])
            
            prev_x = x1
            prev_y = y1            
            for curr_point in curr_path:
                shouldProceed = game_ball.move_component(curr_point[0], curr_point[1], game_paddle)
                if shouldProceed == 2:
                    os.system('aplay -q ./sound_effects/ball_hit_obstacle.wav&')
                    if TIME > LEVEL_TIME_LIMIT:
                        shift_bricks_downwards()
                    break
                if shouldProceed == 0:
                    os.system('aplay -q ./sound_effects/ball_hit_obstacle.wav&')
                if game_ball.can_display_ball():
                    if game_boss_enemy.can_display_boss_enemy():
                        shouldProceed = boss_level_collision_check(curr_point, game_ball, prev_x, prev_y)
                    else:
                        for i in range(len(game_bricks)):
                            if game_bricks[i].can_display_brick():
                                if game_bricks[i].collided(game_ball):
                                    os.system('aplay -q ./sound_effects/ball_hit_obstacle.wav&')
                                    shouldProceed = 0
                                    if game_bricks[i].is_rainbow():
                                        game_bricks[i].set_rainbow_status(False)
                                    rise = game_bricks[i].got_hit(game_ball.is_in_power_mode(), game_bricks, game_ball.is_in_fire_mode())
                                    updateScore(rise)
                                    if game_bricks[i].get_strength() == 0:
                                        generate_power_up(game_bricks[i], game_ball.get_vel_x(), game_ball.get_vel_y())
                                    game_ball.ball_reflection(game_bricks[i], prev_x, prev_y) 
                prev_x = game_ball.get_x()
                prev_y = game_ball.get_y()                            
                if shouldProceed == 0:
                    break

def move_bullets_carefully():
    global game_bricks
    for game_bullet in game_bullets:
        if game_bullet.can_display_bullet():
            ball_vel_x = game_bullet.get_vel_x()
            ball_vel_y = game_bullet.get_vel_y()   
            m = INF  
            c = INF 
            
            if ball_vel_x != 0:
                m = ball_vel_y / ball_vel_x      
            x2 = game_bullet.get_x() + ball_vel_x
            y2 = game_bullet.get_y() + ball_vel_y        
            x1 = game_bullet.get_x()
            y1 = game_bullet.get_y()
            if ball_vel_x != 0:
                c = y1 - (m*x1)
            
            curr_path = []
            if ball_vel_x == 0:
                if y2 > y1:
                    for y_coord in range(y1 + 1, y2 + 1):
                        curr_path.append([x1, y_coord])
                else:
                    for y_coord in range(y1 - 1, y2 - 1, -1):
                        curr_path.append([x1, y_coord])
            else:
                if x2 > x1:
                    for x_coord in range(x1 + 1, x2 + 1):
                        if (((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1) == int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1)):
                            curr_path.append([x_coord, int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1))])
                else:
                    for x_coord in range(x1 - 1, x2 - 1, -1):
                        if (((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1) == int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1)):
                            curr_path.append([x_coord, int(round(((y2 - y1)*(x_coord - x1))/(x2 - x1) + y1))])
            
            for curr_point in curr_path:
                shouldProceed = 1
                game_bullet.move_component(curr_point[0], curr_point[1])
                if game_bullet.can_display_bullet():
                    for i in range(len(game_bricks)):
                        if game_bricks[i].can_display_brick():
                            if game_bricks[i].collided(game_bullet):
                                shouldProceed = 0
                                game_bullet.set_display_status(False)
                                if game_bricks[i].is_rainbow():
                                    game_bricks[i].set_rainbow_status(False)
                                rise = game_bricks[i].got_hit(False, game_bricks, False)
                                updateScore(rise)            
                                if game_bricks[i].get_strength() == 0:
                                    generate_power_up(game_bricks[i], game_bullet.get_vel_x(), game_bullet.get_vel_y())
                if shouldProceed == 0:
                    break
               
def get_all_bricks():
    global game_bricks
    for i in range(len(game_bricks)):
        if game_bricks[i].can_display_brick():
            game_bricks[i].display_component()  
            
def get_balls():
    global game_balls
    for game_ball in game_balls:
        if game_ball.can_display_ball():
            game_ball.display_component()
            
def get_boss_enemy():
    global game_boss_enemy
    global game_boss_enemy_unbreakable_bricks
    global game_boss_enemy_spawned_bricks
    if game_boss_enemy.can_display_boss_enemy():
        game_boss_enemy.display_component()
    for game_boss_enemy_unbreakable_brick in game_boss_enemy_unbreakable_bricks:
        if game_boss_enemy_unbreakable_brick.can_display_brick():
            game_boss_enemy_unbreakable_brick.display_component()
    for game_boss_enemy_spawned_brick in game_boss_enemy_spawned_bricks:
        if game_boss_enemy_spawned_brick.can_display_brick():
            game_boss_enemy_spawned_brick.display_component()
            
def get_bullets():
    global game_bullets
    for game_bullet in game_bullets:
        if game_bullet.can_display_bullet():
            game_bullet.display_component()

def get_cannons():
    global game_cannon_1
    global game_cannon_2
    game_cannon_1.display_component()
    game_cannon_2.display_component()
    
def set_cannons_pos():
    global game_cannon_1
    global game_cannon_2
    global game_paddle
    game_cannon_1.set_x(game_paddle.get_x())
    game_cannon_2.set_x(game_paddle.get_x() + game_paddle.get_paddle_length() - 2)
    
def get_paddle():
    global game_paddle
    game_paddle.display_component()

def there_exist_powerup():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    
    global game_ball_multipliers
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.can_display_power_up():
            return True
    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.can_display_power_up():
            return True
    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.can_display_power_up():
            return True
    for game_thru_ball in game_thru_balls:
        if game_thru_ball.can_display_power_up():
            return True
    for game_fire_ball in game_fire_balls:
        if game_fire_ball.can_display_power_up():
            return True
    for game_fast_ball in game_fast_balls:
        if game_fast_ball.can_display_power_up():
            return True
    for game_ball_multiplier in game_ball_multipliers:
        if game_ball_multiplier.can_display_power_up():
            return True
    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.can_display_power_up():
            return True
    return False
   
def get_power_ups():
    global game_balls
    global game_bricks
    global game_paddle_grabs
    global game_expand_paddles
    global game_shrink_paddles
    global game_thru_balls
    global game_fire_balls
    global game_fast_balls
    global game_shooting_paddles
    global game_ball_multipliers
    
    for game_paddle_grab in game_paddle_grabs:
        if game_paddle_grab.can_display_power_up():
            game_paddle_grab.display_component()
    for game_expand_paddle in game_expand_paddles:
        if game_expand_paddle.can_display_power_up():
            game_expand_paddle.display_component()
    for game_shrink_paddle in game_shrink_paddles:
        if game_shrink_paddle.can_display_power_up():
            game_shrink_paddle.display_component()
    for game_thru_ball in game_thru_balls:
        if game_thru_ball.can_display_power_up():
            game_thru_ball.display_component()
    for game_fire_ball in game_fire_balls:
        if game_fire_ball.can_display_power_up():
            game_fire_ball.display_component()
    for game_fast_ball in game_fast_balls:
        if game_fast_ball.can_display_power_up():
            game_fast_ball.display_component()
    for game_ball_multiplier in game_ball_multipliers:
        if game_ball_multiplier.can_display_power_up():
            game_ball_multiplier.display_component()
    for game_shooting_paddle in game_shooting_paddles:
        if game_shooting_paddle.can_display_power_up():
            game_shooting_paddle.display_component()
            
def get_key():
    getch = Get()
    inp_char = input_to(getch, 0.1)
    return inp_char

def end_game():
    global SCORE
    global LIVES
    global game_bricks
    global game_boss_enemy_spawned_bricks
    global game_boss_enemy_unbreakable_bricks
    global game_arena
    global LEVEL
    global TIME
    global time_of_starting
    global prev_time
    # print("EEEEEEEEEEEEEEEEEEENNNNNNNNNNNNNNNNNDDDDDDDDDDDDDDDDDDDD GGGGGGGGGGGGGAAAAAMMMMMMMMMEEEEEEEEEEEEEEEE")
    
    if did_win():
        if LEVEL < 3:
            LEVEL += 1
            reset_game()
            game_bricks.clear()
            game_boss_enemy_unbreakable_bricks.clear()
            game_boss_enemy_spawned_bricks.clear()
            if LEVEL == 2:
                setup_bricks_second_level()
            else:
                setup_boss_level()
            TIME = 0
            time_of_starting = time.time()
            prev_time = 0
            return 0
        else:
            os.system('aplay -q ./sound_effects/you_won.wav&')
            while True:
                manage_display()
                game_arena.game_over_arena(SCORE, True)
                game_arena.display_arena()
                inp_k = get_key()
                if inp_k == 'q':
                    return -INF
                elif inp_k == 's':
                    return INF          
    else:
        os.system('aplay -q ./sound_effects/you_lost.wav&')    
        while True:
            manage_display()
            game_arena.game_over_arena(SCORE, False)
            game_arena.display_arena()
            inp_k = get_key()
            if inp_k == 'q':
                return -INF
            elif inp_k == 's':
                return INF

def go_to_next_level_abruptly():
    global LEVEL
    global game_bricks
    global game_boss_enemy_spawned_bricks
    global game_boss_enemy_unbreakable_bricks
    global TIME
    global time_of_starting
    global prev_time
    
    if LEVEL < 3:
        LEVEL += 1
        # print("Current Level: " + str(LEVEL))
        reset_game()
        game_bricks.clear()
        game_boss_enemy_unbreakable_bricks.clear()
        game_boss_enemy_spawned_bricks.clear()
        if LEVEL == 2:
            setup_bricks_second_level()
        else:
            # # print("Suckkkkkkkkkkkkkkkkkkkkkkkkk")
            setup_boss_level()
        TIME = 0
        time_of_starting = time.time()
        prev_time = 0
        return 0
    else:
        # print("Black sheeep 4")
        return end_game() 
    
def shift_paddle_to_left(LEVEL):
    global game_balls
    global game_paddle
    global game_cannon_1
    global game_cannon_2
    
    game_paddle.move_component(0, game_balls, game_cannon_1, game_cannon_2, game_boss_enemy, game_boss_enemy_unbreakable_bricks, LEVEL)

def shift_paddle_to_right(LEVEL):
    global game_paddle
    global game_balls
    global game_cannon_1
    global game_cannon_2
    
    game_paddle.move_component(1, game_balls, game_cannon_1, game_cannon_2, game_boss_enemy, game_boss_enemy_unbreakable_bricks, LEVEL)
    
def release_held_balls():
    global game_paddle
    global game_balls
    
    game_paddle.set_grab_balls(False)
    for game_ball in game_balls:
        if game_ball.can_display_ball():
            game_ball.update_movement_status(False)

def intro_time():
    global game_arena
    global time_of_starting
    global prev_time
    while True:
        manage_display()
        game_arena.intro_screen()
        game_arena.display_arena()
        inp_k = get_key()
        if inp_k == 's':
            prev_time = 0
            time_of_starting = time.time()
            break 
        
def finish_game_setup():
    os.system('clear')
    setup_game()
    intro_time()     
    

def brick_breaker_game(): 
    global time_of_starting
    global prev_time
    global game_boss_enemy
    global SHOOTING_PADDLE_TIME_LEFT
    global display_shooting_paddle_timer

    while True:
        inp_key = get_key()
        if inp_key == 'q' or getLives() <= 0:
            # print("Black sheeep 3")
            store = end_game()
            if store == INF:
                finish_game_setup() 
                continue
            elif store == -INF:
                break
        elif inp_key == 'a':
            shift_paddle_to_left(getLevel())
        elif inp_key == 'd':
            shift_paddle_to_right(getLevel())
        elif inp_key == 'l':
            release_held_balls()
        elif inp_key == 'n':
            store = go_to_next_level_abruptly()
            if store == INF:
                finish_game_setup()
                continue
            elif store == -INF:
                break
               
        manage_display()
        TIME = int(round(time.time())) - int(round(time_of_starting))
        
        if getLevel() <= 2 and bricks_reached_paddle_level():
            # print("Black sheeep 2")
            store = end_game()
            if store == INF:
                finish_game_setup() 
                continue
            elif store == -INF:
                break   
        
        if getLevel() <= 2 and all_bricks_done():
            # print("Black sheeep 1")
            store = end_game()
            if store == INF:
                finish_game_setup()
                continue
            elif store == -INF:
                break
            
        if getLevel() == 3 and not game_boss_enemy.can_display_boss_enemy():
            store = end_game()
            if store == INF:
                finish_game_setup()
                continue
            elif store == -INF:
                break   
        
        rainbow_bricks_gimmicks()
        
        #update x and ys here
        if prev_time != TIME:
            powerup_gravity_effect()
        displace_powerups()
        if prev_time != TIME:
            update_power_ups_status()
            if TIME % 2 == 0 and game_boss_enemy.can_display_boss_enemy():
                drop_bombs()
            # if no_shooting_paddle_active():
            #     SHOOTING_PADDLE_TIME_LEFT = 0
            #     display_shooting_paddle_timer = False
        monitor_boss_spawning_bricks()
        move_ball_carefully(TIME)
        move_bullets_carefully()
        if game_boss_enemy.can_display_boss_enemy():
            li = move_bombs()
            if li == INF:
                finish_game_setup()
                continue
            elif li == -INF:
                break
        
        #reset screen here
        liv = updateLives()
        if liv == INF:
            finish_game_setup()
            continue
        elif liv == -INF:
            break
        
        game_arena.refresh_arena(TIME, getScore(), getLives(), getLevel(), display_shooting_paddle_timer, SHOOTING_PADDLE_TIME_LEFT, get_boss_enemy_health_bar())
        
        #display component (adding components) function calls
        get_balls()
        get_bullets()
        get_all_bricks()
        get_paddle()
        get_power_ups()
        if game_boss_enemy.can_display_boss_enemy():
            get_boss_enemy()
            get_bombs()
        
        if display_shooting_paddle_timer:
            game_cannon_1.set_display_status(True)
            game_cannon_2.set_display_status(True)
            set_cannons_pos()
            get_cannons()
        else:
            game_cannon_1.set_display_status(False)
            game_cannon_2.set_display_status(False)
        #display screen
        game_arena.display_arena()
        prev_time = TIME
        
def play_game():
    finish_game_setup()
    brick_breaker_game()