from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math
# Grid ar basic setup - eita khub important
GRID_SIZE = 14
CELL_SIZE = 40
HALF_CELL = CELL_SIZE // 2
GRID_LENGTH = GRID_SIZE * CELL_SIZE
GRID_OFFSET = GRID_LENGTH // 2

# Minimap er jonno - corner e choto ekta map dekhano hobe
MINIMAP_SIZE = 150
MINIMAP_OFFSET_X = 820
MINIMAP_OFFSET_Y = 620
MINIMAP_CELL_SIZE = MINIMAP_SIZE // GRID_SIZE

# Camera settings - third person theke first person switch korte parbo
camera_pos = (0, -500, 400)
camera_distance = 500
camera_height = 400
camera_angle = 0
camera_fov = 60
is_first_person = False
first_person_height = 20
zoom_speed = 20
rotation_speed = 3
fovY = 60

# Game er different states - start menu, playing, paused etc
game_state = "START_MENU"
difficulty = "NORMAL"  # NORMAL theke PUNISHER porjonto
game_mode = "SURVIVAL"  # Different modes ache
snake_skin_color = "GREEN"

# Quick play mode er jonno timer - 90 second time limit
quick_play_duration = 90
game_start_time = 0
time_remaining = 0

# Snake er main data - position, direction, speed sob kichu
snake_positions = [(GRID_SIZE // 2, GRID_SIZE // 2)]  # Middle e start korbe
snake_direction = (1, 0)  # Right dike jabe initially
snake_speed = 0.01
last_move_time = 0

# Different snake colors - player choose korte parbe
snake_colors = {
    "GREEN": (0.0, 0.8, 0.2),
    "BLUE": (0.2, 0.4, 0.8),
    "RED": (0.8, 0.2, 0.2),
    "YELLOW": (0.8, 0.8, 0.2),
    "PURPLE": (0.6, 0.2, 0.8)
}

# Food system - normal ar special food dui type ache
food_position = None
special_food_position = None
special_food_type = None  # SPEED, DOUBLE_POINTS, INVINCIBILITY

# Special power-up effects - temporary boost gulo
special_effects = {
    "speed_boost": False,
    "double_points": False,
    "invincibility": False,
    "effect_start_time": 0,
    "effect_duration": 10  # 10 second cholbe effect
}

# Game elements - obstacles ar bombs dangerous
obstacles = []
bombs = []
score = 0
fruits_collected = 0
level = 1
food_eaten = 0

# Cheat codes - debugging ar testing er jonno rakhlam
cheat_mode = False
cheat_invincibility = False
cheat_speed_control = False

# Background atmosphere colors - score onujayi change hobe
atmosphere_colors = {
    "BLUE": (0.4, 0.6, 1.0, 1.0),
    "YELLOW": (1.0, 1.0, 0.4, 1.0),
    "RED": (1.0, 0.4, 0.4, 1.0),
    "GREEN": (0.4, 1.0, 0.4, 1.0)
}

current_atmosphere = "BLUE"

# UI buttons - menu gulo handle korar jonno
buttons = {
    "play": {"x": 400, "y": 400, "w": 200, "h": 50, "text": "PLAY GAME"},
    "difficulty": {"x": 400, "y": 330, "w": 200, "h": 50, "text": "DIFFICULTY: NORMAL"},
    "game_mode": {"x": 400, "y": 260, "w": 200, "h": 50, "text": "MODE: SURVIVAL"},
    "snake_color": {"x": 400, "y": 190, "w": 200, "h": 50, "text": "SNAKE: GREEN"},
    "pause": {"x": 850, "y": 750, "w": 100, "h": 40, "text": "PAUSE"},
    "resume": {"x": 850, "y": 750, "w": 100, "h": 40, "text": "RESUME"},
    "restart": {"x": 400, "y": 350, "w": 200, "h": 50, "text": "RESTART"},
    "main_menu": {"x": 400, "y": 280, "w": 200, "h": 50, "text": "MAIN MENU"}
}





def convert_screen_coords(x, y):
    # Screen coordinate ke game coordinate e convert kore
    return x, 800 - y


def setup_2d_rendering():
    # UI drawing er jonno 2D mode e switch
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1000, 0, 800, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

def restore_3d_rendering():
    # Abar 3D mode e fire jabe
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    # Text draw korar simple function
    setup_2d_rendering()
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    restore_3d_rendering()

def draw_button(button_name, button_data, is_active=True):
    # Menu button draw kore - clicking er jonno
    if not is_active:
        return

    setup_2d_rendering()
    x, y, w, h = button_data["x"], button_data["y"], button_data["w"], button_data["h"]

    # Button background
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y - h)
    glVertex2f(x, y - h)
    glEnd()

    # Button border
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y - h)
    glVertex2f(x, y - h)
    glEnd()

    # Button text center e
    text_x = x + (w - len(button_data["text"]) * 8) // 2
    text_y = y - h // 2 - 5
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(text_x, text_y)
    for char in button_data["text"]:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    restore_3d_rendering()

def check_quick_play_timer():
    # Quick play mode er 90 second timer check
    global time_remaining, game_state

    if game_mode == "QUICK_PLAY" and game_state == "PLAYING":
        current_time = time.time()
        elapsed_time = current_time - game_start_time
        time_remaining = max(0, quick_play_duration - elapsed_time)

        if time_remaining <= 0:
            game_over()  # Time shesh - game over
def game_over():
    # Game shesh hole cleanup
    global game_state, special_effects
    game_state = "GAME_OVER"

    # All effects off
    for effect in special_effects:
        if effect != "effect_duration":
            special_effects[effect] = False

def reset_game():
    # Notun game shuru korar jonno sob reset
    global snake_positions, snake_direction, score, level, food_eaten, last_move_time
    global food_position, special_food_position, special_food_type, special_effects
    global obstacles, bombs, current_atmosphere, fruits_collected, game_start_time, time_remaining

    snake_positions = [(GRID_SIZE // 2, GRID_SIZE // 2)]  # Center e start
    snake_direction = (1, 0)  # Right dike

    score = 0
    level = 1
    food_eaten = 0
    fruits_collected = 0
    last_move_time = 0

    if game_mode == "QUICK_PLAY":
        game_start_time = time.time()
        time_remaining = quick_play_duration

    food_position = None
    special_food_position = None
    special_food_type = None

    # All effects clear
    for effect in special_effects:
        if effect != "effect_duration":
            special_effects[effect] = False

    obstacles = []
    bombs = []
    current_atmosphere = "BLUE"

    # Initial setup
    generate_food()
    generate_obstacles()
    if difficulty != "NORMAL" or game_mode != "QUICK_PLAY":
        generate_bombs()

    set_snake_speed()
    update_atmosphere()

def draw_start_menu():
    # Main menu - instructions ar settings
    draw_text(450, 600, "VIPER 3D", GLUT_BITMAP_TIMES_ROMAN_24)

    instructions = [
        "Use Arrow Keys to move the snake",
        "Eat red apples to grow and score points",
        "Collect special stars for power-ups:",
        "  - Blue Star: Speed Boost",
        "  - Orange Star: Double Points",
        "  - Yellow Star: Invincibility",
        "Avoid obstacles (gray blocks) and bombs (black spheres)",
        "",
        "Game Modes:",
        "  - SURVIVAL: Classic mode with growing snake",
        "  - QUICK_PLAY: 90-second fruit collection challenge",
        "  - BORDERLESS: Walls don't kill you",
        "",
        "Controls:",
        "P/Space: Pause/Resume (not in Quick Play)",
        "V: Toggle First/Third Person View",
        "R: Restart Game",
        "W/S: Camera Height (Third Person)",
        "X/Y: Zoom In/Out (Third Person)",
        "",
        "Cheat Mode (Press C):",
        "I: Toggle Invincibility",
        "O: Toggle Speed Control"
    ]

    y_pos = 500
    for instruction in instructions:
        draw_text(50, y_pos, instruction, GLUT_BITMAP_HELVETICA_12)
        y_pos -= 20

    # Menu buttons
    draw_button("play", buttons["play"])
    draw_button("difficulty", buttons["difficulty"])
    draw_button("game_mode", buttons["game_mode"])
    draw_button("snake_color", buttons["snake_color"])

def draw_game_over_screen():
    # Game over screen - transparent overlay
    setup_2d_rendering()

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.0, 0.0, 0.0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)
    glVertex2f(1000, 800)
    glVertex2f(0, 800)
    glEnd()

    restore_3d_rendering()

    draw_text(420, 500, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)

    # Different messages for different modes
    if game_mode == "QUICK_PLAY":
        draw_text(380, 460, f"Time's Up!")
        draw_text(350, 430, f"Fruits Collected: {fruits_collected}")
        draw_text(380, 400, f"Final Score: {score}")

        # Performance rating system - motivation er jonno
        if fruits_collected >= 20:
            rating = "AMAZING!"
        elif fruits_collected >= 15:
            rating = "EXCELLENT!"
        elif fruits_collected >= 10:
            rating = "GOOD!"
        elif fruits_collected >= 5:
            rating = "NOT BAD"
        else:
            rating = "KEEP TRYING!"

        draw_text(400, 370, f"Rating: {rating}")
    else:
        draw_text(380, 460, f"Final Score: {score}")
        draw_text(370, 430, f"Level Reached: {level}")

    draw_button("restart", buttons["restart"])
    draw_button("main_menu", buttons["main_menu"])
def draw_paused_screen():
    # Pause screen - simple overlay
    setup_2d_rendering()

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.0, 0.0, 0.0, 0.5)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)
    glVertex2f(1000, 800)
    glVertex2f(0, 800)
    glEnd()

    restore_3d_rendering()

    draw_text(450, 400, "PAUSED", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 360, "Press P or Space to resume")
    draw_button("resume", buttons["resume"])
def draw_hud():
    # HUD info - game statistics ar current status
    if game_state in ["PLAYING", "PAUSED"]:
        draw_text(10, 770, f"Score: {score}")

        if game_mode == "QUICK_PLAY":
            # Timer display - MM:SS format
            minutes = int(time_remaining // 60)
            seconds = int(time_remaining % 60)
            draw_text(10, 740, f"Time: {minutes:02d}:{seconds:02d}")
            draw_text(10, 710, f"Fruits: {fruits_collected}")
        else:
            draw_text(10, 740, f"Level: {level}")

        draw_text(10, 680, f"Difficulty: {difficulty}")
        draw_text(10, 650, f"Mode: {game_mode}")
        draw_text(10, 620, f"Snake: {snake_skin_color}")

        camera_mode = "First Person" if is_first_person else "Third Person"
        draw_text(10, 590, f"Camera: {camera_mode}")

        # Active effects display - remaining time shohho
        y_offset = 560
        if special_effects["speed_boost"]:
            remaining = special_effects["effect_duration"] - (time.time() - special_effects["effect_start_time"])
            draw_text(10, y_offset, f"Speed Boost: {remaining:.1f}s")
            y_offset -= 30

        if special_effects["double_points"]:
            remaining = special_effects["effect_duration"] - (time.time() - special_effects["effect_start_time"])
            draw_text(10, y_offset, f"Double Points: {remaining:.1f}s")
            y_offset -= 30

        if special_effects["invincibility"]:
            remaining = special_effects["effect_duration"] - (time.time() - special_effects["effect_start_time"])
            draw_text(10, y_offset, f"Invincibility: {remaining:.1f}s")
            y_offset -= 30

        # Cheat mode indicators
        if cheat_mode:
            draw_text(10, y_offset, "CHEAT MODE ACTIVE")
            y_offset -= 30
            if cheat_invincibility:
                draw_text(10, y_offset, "Cheat Invincibility: ON")
                y_offset -= 30
            if cheat_speed_control:
                draw_text(10, y_offset, "Cheat Speed: ON")
                y_offset -= 30

def mouseListener(button, state, x, y):
    # Mouse click handler - menu interactions
    global game_state, difficulty, game_mode, snake_skin_color

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_x, mouse_y = convert_screen_coords(x, y)

        if game_state == "START_MENU":
            # Play button
            if (buttons["play"]["x"] <= mouse_x <= buttons["play"]["x"] + buttons["play"]["w"] and
                    buttons["play"]["y"] - buttons["play"]["h"] <= mouse_y <= buttons["play"]["y"]):
                reset_game()
                game_state = "PLAYING"

            # Difficulty cycle
            elif (buttons["difficulty"]["x"] <= mouse_x <= buttons["difficulty"]["x"] + buttons["difficulty"]["w"] and
                  buttons["difficulty"]["y"] - buttons["difficulty"]["h"] <= mouse_y <= buttons["difficulty"]["y"]):
                if difficulty == "NORMAL":
                    difficulty = "HARD"
                elif difficulty == "HARD":
                    difficulty = "PUNISHER"
                else:
                    difficulty = "NORMAL"
                buttons["difficulty"]["text"] = f"DIFFICULTY: {difficulty}"

            # Game mode cycle
            elif (buttons["game_mode"]["x"] <= mouse_x <= buttons["game_mode"]["x"] + buttons["game_mode"]["w"] and
                  buttons["game_mode"]["y"] - buttons["game_mode"]["h"] <= mouse_y <= buttons["game_mode"]["y"]):
                if game_mode == "SURVIVAL":
                    game_mode = "QUICK_PLAY"
                elif game_mode == "QUICK_PLAY":
                    game_mode = "BORDERLESS"
                else:
                    game_mode = "SURVIVAL"
                buttons["game_mode"]["text"] = f"MODE: {game_mode}"

            # Snake color cycle
            elif (buttons["snake_color"]["x"] <= mouse_x <= buttons["snake_color"]["x"] + buttons["snake_color"]["w"] and
                  buttons["snake_color"]["y"] - buttons["snake_color"]["h"] <= mouse_y <= buttons["snake_color"]["y"]):
                colors = list(snake_colors.keys())
                current_index = colors.index(snake_skin_color)
                snake_skin_color = colors[(current_index + 1) % len(colors)]
                buttons["snake_color"]["text"] = f"SNAKE: {snake_skin_color}"

        elif game_state == "PLAYING":
            # Pause button - quick play e nai
            if game_mode != "QUICK_PLAY":
                if (buttons["pause"]["x"] <= mouse_x <= buttons["pause"]["x"] + buttons["pause"]["w"] and
                        buttons["pause"]["y"] - buttons["pause"]["h"] <= mouse_y <= buttons["pause"]["y"]):
                    game_state = "PAUSED"

        elif game_state == "PAUSED":
            # Resume button
            if (buttons["resume"]["x"] <= mouse_x <= buttons["resume"]["x"] + buttons["resume"]["w"] and
                    buttons["resume"]["y"] - buttons["resume"]["h"] <= mouse_y <= buttons["resume"]["y"]):
                game_state = "PLAYING"

        elif game_state == "GAME_OVER":
            # Restart button
            if (buttons["restart"]["x"] <= mouse_x <= buttons["restart"]["x"] + buttons["restart"]["w"] and
                    buttons["restart"]["y"] - buttons["restart"]["h"] <= mouse_y <= buttons["restart"]["y"]):
                reset_game()
                game_state = "PLAYING"

            # Main menu button
            elif (buttons["main_menu"]["x"] <= mouse_x <= buttons["main_menu"]["x"] + buttons["main_menu"]["w"] and
                  buttons["main_menu"]["y"] - buttons["main_menu"]["h"] <= mouse_y <= buttons["main_menu"]["y"]):
                game_state = "START_MENU"
