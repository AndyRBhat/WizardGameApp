from mylibrary import *
from random import randint, choice

# --- GAME SETUP & ASSETS ---
# Set the background and load the main character
add_background("images/grass_field.png")
wizard = add_image("images/wizard1.gif", 50) # Wizard size is 50px

# Initialize wizard starting position (center-ish)
start_x = 425
start_y = 275
position_element(wizard, start_x, start_y)

# Set Game Duration (135 seconds)
game_time=135
timer_text = add_text(f"Time Left: {game_time}")
position_element(timer_text, "right", "top")

# --- AUDIO LOADING ---
# Background music loops automatically
add_background_audio("audio/game-music.mp3")

# Pre-load sound effects for interaction events
ouch_sound = add_audio("audio/ouch.mp3")
winning_sound = add_audio("audio/winning.mp3")
losing_sound = add_audio("audio/losing.mp3")

# --- GLOBAL STATE VARIABLES ---
# Track the wizard's current position
x = start_x
y = start_y

# Enemy configuration
enemies = ["images/zombie1.gif", "images/bat.gif", "images/creature2.webp"]
wizard_health=100
health_text=add_text(f"Health: {wizard_health}", 20)
position_element(health_text, "left", "top")

# --- CORE GAME FUNCTIONS ---
def countdown():
    """
    Called every 1 second. Updates the timer and triggers enemy spawns.
    """
    global game_time
    game_time-=1

    # Spawn new enemies every second
    add_enemy()

    # Update the timer UI
    update_text(timer_text, f"Time Left: {game_time}")
def win_game():
    """
    Triggered when the timer runs out successfully.
    """   
    clear()
    play_audio(winning_sound)
    win_text= add_text("You survived! You win!", 65)
    position_element(win_text,"center", "center")
    
def move_wizard(key):
    """
    Handles WASD input to move the wizard.
    Includes boundary checks to keep the player on the 950x550 screen.
    """
    global x
    global y
    distance = 10
    if key == "w":
        if y > distance:
            y -= distance
    elif key == "a":
        if x > distance:
            x -= distance
    elif key == "s":
        if y < 550 - distance:
            y += distance
    elif key == "d":
        if x < 950 - distance:
            x += distance       
    
    # Apply the new coordinates to the HTML element
    position_element(wizard, x, y)

def add_enemy():  
    """
    Spawns enemies at random locations outside the screen and animates them inward.
    Includes 'Difficulty Scaling' to increase spawn rate as time decreases.
    """ 
    def place_enemy():
        # Select random sprite and spawn location
        random_enemy = choice(enemies)
        enemy = add_image(random_enemy, 75)
        random_x = randint(1, 1000)
        random_y = randint(1, 1000)
        direction = randint(1, 4)
        # Determine start side (Top, Left, Bottom, Right)
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

        # Collision listener for this specific enemy
        check_collision(wizard, enemy, subtract_wizard_hp)

    def animate_enemy(enemy, start_position):
        """Moves the enemy across the screen based on where it spawned."""
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
    # --- DIFFICULTY SCALING ---
    # As game_time decreases, the number of enemies spawned per second increases.
    if game_time<=100:
        for num in range(2):
            place_enemy()
    elif game_time<=60:
        for num in range(4):
            place_enemy()
    elif game_time<=30:
        for num in range(8):
            place_enemy()
    else:
        for num in range(1):
            place_enemy()

def game_over():
    """Triggered when health reaches 0."""
    clear()
    play_audio(losing_sound)
    game_over_text= add_text("Game Over! You Lose!", 65)
    position_element(game_over_text, "center", "center")

def subtract_wizard_hp():
    """
    Callback function when a collision occurs.
    Updates health, plays sound, and checks for loss condition.
    """
    global wizard_health
    play_audio(ouch_sound)
    wizard_health-=0.5
    update_text(health_text, f"Health: {round(wizard_health)}")
    if wizard_health <= 0:
        game_over()
# --- GAME LOOP INITIALIZATION ---
# Start the countdown timer (runs every 1 second)
set_interval(countdown, 1)
# Set the win condition timer
set_timeout(win_game, game_time)
# Initial enemy spawn
add_enemy()
# Begin listening for keyboard input
keydown(move_wizard)