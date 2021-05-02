# ASSIGNMENT-3: BRICK-BREAKER

## Name - Gokul Vamsi Thota
## Roll number - 2019111009



### Brief Description

This game is a terminal version of the classic 'Brick-Breaker' Game. This game involves destroying bricks with a ball, and the support of a paddle, and helpful powerups. Do refrain from playing this game if you have epilepsy (or watch out for the rainbow bricks xD).



### Running the code

Only external library required to be installed for running this code is colorama, which can be installed with the command: `pip3 install colorama`
For playing the game, follow the instructions below:

* After extracting the folder into some location on your system, enter the directory 2019111009, with the command: `cd 2019111009`

* To start playing the game, run the command: `python3 main.py`

* Please note that the game is designed to fit perfectly into the full-screen mode of terminal window (The values of height and width in heads.py file can be altered). The colour preferred is default color of vim terminal (maroon).



### Important Instructions

* Press 'a' key to move the paddle one unit to the left

* Press 'd' key to move the paddle one unit to the right

* Press 'q' key to quit the game at any point

* Press 'l' key to release the ball from the paddle, at the beginning of the level, where the ball is stuck to the paddle; or when the 'paddle grab' powerup is activated and the ball is currently stuck on the paddle. Note that even when this powerup is deactivated, the ball would be released only if this key is pressed. 

* Press 's' to start the game (when initial screen is displayed)

* Press 'n' key to skip directly to the next level. Game ends when this is pressed in the last level.

* There are 3 levels, each harder than the previous one.

* There are 12 lives in total.

* In first 2 levels, destroy all the bricks with the ball, with the help of powerups and paddle

* In the final level, decrease boss enemy's health to 0 with the power of the ball and win the game!





### Points to remember (GAME GUIDE)

* The strengths of the bricks and their corresponding colors are:
<ul><li>Strength = 1 ----- Color = BLUE</li><li>Strength = 2 ----- Color = GREEN</li><li>Strength = 3 ----- Color = YELLOW</li><li>Unbreakable----- Color = RED</li><li>Explosive ----- Color = YELLOW with RED text saying 'TNT'</li></ul>

* Rainbow bricks (specific chosen ones), keep changing colors and strengths till the first time they are hit, and when this happens, their color and strength at that point of impact are considered for future impacts.

* The powerups denoted by particular alphabets in square boxes are:
<ul><li>Thru Ball ----- 'T'</li><li>Shrink Paddle ----- 'S'</li><li>Expand Paddle ----- 'E'</li><li>Paddle Grab ----- 'G'</li><li>Fast Ball ----- 'F'</li><li>Ball Multiplier ----- 'x2'</li><li>Shooting Paddle ----- 'SP'</li><li>Fire Ball ----- 'FB'</li></ul>

* When there are only unbreakable bricks left (in levels 1 and 2), and the player doesn't have and can't collect any powerups, he is expected to quit the game at that point voluntarily, by pressing 'q' or continue playing till he loses (he cannot win that round anyway).

* User won't be getting any powerups in level 3, and wins only when boss enemy health becomes 0. Other instructions of handling is done as in assignment pdf.

* Exploding breaks are denoted separately (in levels 1 and 2), and there are 6 of them in one connected component, and when the ball hits any of these 6, all these exploding bricks along with their corresponding neighbours (diagonal, horizontal and vertical) are destroyed. 

* When fireball powerup is activated, every brick that comes in contact with the ball is treated as an exploding brick.

* Bricks start falling by one unit in the first two levels, after the user spent 30 seconds in that level.

* In the third level, bricks are spawned by boss first when his health decreases below 5 and is spawned again when more than 66% of previous ones are destroyed.

* There are 12 lives available to the player in total, and if the player manages to destroy all the bricks before exhausting these lives (levels 1 and 2), he is considered as 'winner' of that level, and he progresses further. He is said to win the game when he further defeats the boss enemy in the final level, otherwise he is said to 'lose' the game. In either cases, score is displayed at the end. (Player loses if he quits in the middle of the game)

* Powerups move with gravity effect, and when they are successfully obtained by the paddle, they are active for 12 seconds. When more number of powerups are collected, only the effect of the powerup increases (it won't be active for sum of all remaining durations for powerups of that type).




### Implementation

* All the features as mentioned in the assignment pdf, are strictly adhered to, and implemented (including the bonus features 'Exploding bricks', 'fire ball', 'sound effects')

* Apt sound effects are used throughout the game.

* Collisions between ball and bricks, ball and walls are elastic; whereas collisions between ball and paddle is handled as explained in the pdf.

* Collisions with boss enemy are handled in same way above. Initial health of boss enemy is 12 and decreases by one with one impact from ball.

* Powerups (with self explanatory functionalities), are affected only by the paddle, and are activated only when collected by the paddle, and are deactivated after a fixed duration of time.

* Score is calculated with respect to the number of destroyed bricks and their strength (handled specially when explosive bricks are hit) in the first 2 levels, and based on the collisions with the boss enemy in last level.

* The code has modular structure, with individual classes defined for individual game objects like the game arena (game screen), ball, paddle, bricks and each individual powerup, along with boss enemy, bullets, bombs etc.

* Inheritance is followed at necessary places, such as 'Ball', 'Brick', 'PowerUp' and 'Paddle' Classes inheriting common features from 'Component' class, and the individual PowerUps (8 in number) inheriting features from class 'PowerUp'

* Polymorphism is followed at necessary places, such as functions like 'display_component' and 'move_component' of the 'Component' Class are overriden in classes like 'Ball', 'Paddle', 'PowerUp' etc.

* Encapsulation is followed thoroughly in every class, as private and protected fields are used, accessed and updated accordingly.

* Abstraction is achieved in interaction among different game objects, with the help of well defined high-level helper functions defined in the file 'helper.py'.

