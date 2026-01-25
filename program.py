from wizardlib import *
from random import randint, choice
add_background("images/grass_field.png")
wizard = add_image("images/wizard1.gif", 50)
start_x = 425
start_y = 275
position_element(wizard, start_x, start_y)
game_time=135
timer_text = add_text(f"Time Left: {game_time}")
position_element(timer_text, "right", "top")
add_background_audio("audio/game-music.mp3")

x = start_x
y = start_y

enemies = ["images/zombie1.gif", "images/bat.gif", "images/creature2.webp"]
wizard_health=100
health_text=add_text(f"Health: {wizard_health}", 20)
position_element(health_text, "left", "top")
def countdown():
    global game_time
    game_time-=1
    add_enemy()
    update_text(timer_text, f"Time Left: {game_time}")
def win_game():
    clear()
    win_text= add_text("You survived! You win!", 65)
    position_element(win_text,"center", "center")
    
def move_wizard(key):
    global x
    global y
    distance = 10
    if key == "w":
        y -= distance
    elif key == "a":
        x -= distance
    elif key == "s":
        y += distance
    elif key == "d":
        x += distance       
    position_element(wizard, x, y)

def add_enemy():   
    def place_enemy():
        random_enemy = choice(enemies)
        enemy = add_image(random_enemy, 75)
        random_x = randint(1, 1000)
        random_y = randint(1, 1000)
        direction = randint(1, 4)
        if direction == 1:
            position_element(enemy, random_x, -100)
            start_position = "top"
        elif direction == 2:
            position_element(enemy, -100, random_y)
            start_position = "left"
        elif direction == 3:
            position_element(enemy, random_x, 1000)
            start_position = "bottom"
        else:
            position_element(enemy, 1000, random_y)
            start_position = "right"
        animate_enemy(enemy, start_position)
        check_collision(wizard, enemy, subtract_wizard_hp)
    def animate_enemy(enemy, start_position):
        distance = 1200
        time = 10
        if start_position == "top":
            animate_down(enemy, distance, time, False)
        elif start_position == "left":
            animate_right(enemy,distance, time, False) 
        elif start_position == "bottom":
            animate_up(enemy, distance, time, False) 
        elif start_position == "right":
            animate_left(enemy, distance, time, False)
    
    if game_time<=100:
        for num in range(5):
            place_enemy()
    elif game_time<=60:
        for num in range(10):
            place_enemy()
    elif game_time<=30:
        for num in range(20):
            place_enemy()
    else:
        for num in range(3):
            place_enemy()
set_interval(countdown, 1)
set_timeout(win_game, game_time)
def game_over():
    clear()
    game_over_text= add_text("Game Over! You Lose!", 65)
    position_element(game_over_text, "center", "center")
def subtract_wizard_hp():
    global wizard_health
    wizard_health-=0.5
    update_text(health_text, f"Health: {round(wizard_health)}")
    if wizard_health <= 0:
        game_over()
add_enemy()
add_enemy()
add_enemy()
keydown(move_wizard)