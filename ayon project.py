def setupCamera():
    # Camera setup - perspective ar position
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # First person - snake er head theke dekhbe
    if is_first_person and game_state == "PLAYING":
        if not snake_positions:
            return

        head_x, head_y = snake_positions[0]
        dir_x, dir_y = snake_direction

        world_x, world_y = convert_world_coords(head_x, head_y)

        # Snake er direction e look korbe
        look_x = world_x + dir_x * CELL_SIZE * 3
        look_y = world_y + dir_y * CELL_SIZE * 3

        gluLookAt(world_x, world_y, first_person_height,
                  look_x, look_y, first_person_height,
                  0, 0, 1)
    else:
        # Third person - upor theke dekhbe
        x, y, z = camera_pos
        gluLookAt(x, y, z,
                  0, 0, 0,
                  0, 0, 1)
        
def keyboardListener(key, x, y):
    # Keyboard input handle - main controls
    global game_state, camera_distance, camera_height, camera_angle
    global cheat_mode, cheat_invincibility, cheat_speed_control, is_first_person
    global camera_pos

    if key == b'r':  # Restart
        if game_state in ["PLAYING", "PAUSED", "GAME_OVER"]:
            reset_game()
            game_state = "PLAYING"

    elif key == b'p' or key == b' ':  # Pause toggle
        if game_mode != "QUICK_PLAY":  # Quick play e pause nai
            if game_state == "PLAYING":
                game_state = "PAUSED"
            elif game_state == "PAUSED":
                game_state = "PLAYING"

    elif key == b'v':  # Camera view toggle
        is_first_person = not is_first_person

    elif key == b'c':  # Cheat mode toggle
        cheat_mode = not cheat_mode
        if not cheat_mode:
            cheat_invincibility = False
            cheat_speed_control = False

    elif key == b'i' and cheat_mode:  # Invincibility cheat
        cheat_invincibility = not cheat_invincibility

    elif key == b'o' and cheat_mode:  # Speed cheat
        cheat_speed_control = not cheat_speed_control
        set_snake_speed()

    # Camera controls - third person mode e
    elif key == b'x' and not is_first_person:  # Zoom in
        camera_distance = max(200, camera_distance - zoom_speed)
        x, y, z = camera_pos
        camera_pos = (0, -camera_distance, camera_height)

    elif key == b'y' and not is_first_person:  # Zoom out
        camera_distance = min(1000, camera_distance + zoom_speed)
        x, y, z = camera_pos
        camera_pos = (0, -camera_distance, camera_height)

    elif key == b'w' and not is_first_person:  # Camera up
        camera_height = min(800, camera_height + zoom_speed)
        x, y, z = camera_pos
        camera_pos = (0, -camera_distance, camera_height)

    elif key == b's' and not is_first_person:  # Camera down
        camera_height = max(100, camera_height - zoom_speed)
        x, y, z = camera_pos
        camera_pos = (0, -camera_distance, camera_height)

    elif key == b'a' and not is_first_person:  # Rotate left
        camera_angle = (camera_angle + rotation_speed) % 360

    elif key == b'd' and not is_first_person:  # Rotate right
        camera_angle = (camera_angle - rotation_speed) % 360
        
        
def specialKeyListener(key, x, y):
    # Arrow key input - snake movement
    global snake_direction

    if game_state != "PLAYING":
        return

    # First person mode e relative movement
    if is_first_person:
        if key == GLUT_KEY_LEFT:  # Turn left
            dir_x, dir_y = snake_direction
            snake_direction = (-dir_y, dir_x)
        elif key == GLUT_KEY_RIGHT:  # Turn right
            dir_x, dir_y = snake_direction
            snake_direction = (dir_y, -dir_x)
        elif key == GLUT_KEY_DOWN:  # U-turn
            dir_x, dir_y = snake_direction
            snake_direction = (-dir_x, -dir_y)
    else:
        # Third person mode e absolute movement
        new_direction = None

        if key == GLUT_KEY_UP:
            new_direction = (0, 1)
        elif key == GLUT_KEY_DOWN:
            new_direction = (0, -1)
        elif key == GLUT_KEY_LEFT:
            new_direction = (-1, 0)
        elif key == GLUT_KEY_RIGHT:
            new_direction = (1, 0)

        # Prevent immediate reverse - suicide prevention
        if new_direction and len(snake_positions) > 1:
            opposite = (-snake_direction[0], -snake_direction[1])
            if new_direction != opposite:
                snake_direction = new_direction
        elif new_direction and len(snake_positions) == 1:
            snake_direction = new_direction
def draw_minimap():
    # First person mode e corner e minimap dekhabe - besh useful
    if not is_first_person or game_state != "PLAYING":
        return

    setup_2d_rendering()

    # Minimap background - transparent kala
    glColor4f(0.0, 0.0, 0.0, 0.7)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glVertex2f(MINIMAP_OFFSET_X - 5, MINIMAP_OFFSET_Y + 5)
    glVertex2f(MINIMAP_OFFSET_X + MINIMAP_SIZE + 5, MINIMAP_OFFSET_Y + 5)
    glVertex2f(MINIMAP_OFFSET_X + MINIMAP_SIZE + 5, MINIMAP_OFFSET_Y - MINIMAP_SIZE - 5)
    glVertex2f(MINIMAP_OFFSET_X - 5, MINIMAP_OFFSET_Y - MINIMAP_SIZE - 5)
    glEnd()

    # Minimap border
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(MINIMAP_OFFSET_X, MINIMAP_OFFSET_Y)
    glVertex2f(MINIMAP_OFFSET_X + MINIMAP_SIZE, MINIMAP_OFFSET_Y)
    glVertex2f(MINIMAP_OFFSET_X + MINIMAP_SIZE, MINIMAP_OFFSET_Y - MINIMAP_SIZE)
    glVertex2f(MINIMAP_OFFSET_X, MINIMAP_OFFSET_Y - MINIMAP_SIZE)
    glEnd()

    # Grid lines draw
    glColor3f(0.3, 0.3, 0.3)
    for i in range(GRID_SIZE + 1):
        x = MINIMAP_OFFSET_X + i * MINIMAP_CELL_SIZE
        glBegin(GL_LINES)
        glVertex2f(x, MINIMAP_OFFSET_Y)
        glVertex2f(x, MINIMAP_OFFSET_Y - MINIMAP_SIZE)
        glEnd()

        y = MINIMAP_OFFSET_Y - i * MINIMAP_CELL_SIZE
        glBegin(GL_LINES)
        glVertex2f(MINIMAP_OFFSET_X, y)
        glVertex2f(MINIMAP_OFFSET_X + MINIMAP_SIZE, y)
        glEnd()
    def draw_grid():
    # Chess board er moto grid - green shades use korlam
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            world_x, world_y = convert_world_coords(x, y)

            # Alternating colors for checkerboard effect
            if (x + y) % 2 == 0:
                glColor3f(0.3, 0.5, 0.3)
            else:
                glColor3f(0.5, 0.7, 0.5)

            glPushMatrix()
            glTranslatef(world_x, world_y, 0)

            glBegin(GL_QUADS)
            glVertex3f(-HALF_CELL, -HALF_CELL, 0)
            glVertex3f(HALF_CELL, -HALF_CELL, 0)
            glVertex3f(HALF_CELL, HALF_CELL, 0)
            glVertex3f(-HALF_CELL, HALF_CELL, 0)
            glEnd()

            glPopMatrix()
    def update_atmosphere():
    # Score onujayi background color change - progression feel dite
    global current_atmosphere

    if score < 10:
        current_atmosphere = "BLUE"
    elif score < 25:
        current_atmosphere = "YELLOW"
    elif score < 50:
        current_atmosphere = "RED"
    else:
        current_atmosphere = "GREEN"

    glClearColor(*atmosphere_colors[current_atmosphere])

def set_snake_speed():
    # Difficulty ar mode onujayi speed set - important function
    global snake_speed

    base_speeds = {"NORMAL": 0.3, "HARD": 0.2, "PUNISHER": 0.15}
    snake_speed = base_speeds[difficulty]

    if game_mode == "QUICK_PLAY":
        snake_speed *= 0.7  # Quick play e ektu aste

    if cheat_speed_control:
        snake_speed *= 2  # Cheat active hole fast

    if special_effects["speed_boost"]:
        snake_speed *= 0.7  # Speed boost active hole aro fast
              
def normalize_position(x, y):
    # Borderless mode e wall cross korle opposite side e chole jabe
    if game_mode == "BORDERLESS":
        return x % GRID_SIZE, y % GRID_SIZE
    return x, y                  
            