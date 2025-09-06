def draw_snake():
    # Snake drawing - head e chokh mukh, body simple
    if not snake_positions:
        return

    color = snake_colors[snake_skin_color]

    # Special effects hole color change hobe
    if special_effects["invincibility"]:
        glColor3f(1.0, 1.0, 0.0)  # Golden
    elif special_effects["speed_boost"]:
        glColor3f(0.0, 1.0, 1.0)  # Cyan
    elif special_effects["double_points"]:
        glColor3f(1.0, 0.5, 1.0)  # Pink
    else:
        glColor3f(*color)

    # Snake head - sphere with eyes
    head_x, head_y = snake_positions[0]
    world_x, world_y = convert_world_coords(head_x, head_y)

    glPushMatrix()
    glTranslatef(world_x, world_y, HALF_CELL)

    # Head rotation based on direction - realistic lagbe
    dir_x, dir_y = snake_direction
    if dir_x == 1 and dir_y == 0:  # Right
        glRotatef(0, 0, 0, 1)
    elif dir_x == -1 and dir_y == 0:  # Left
        glRotatef(180, 0, 0, 1)
    elif dir_x == 0 and dir_y == 1:  # Up
        glRotatef(90, 0, 0, 1)
    elif dir_x == 0 and dir_y == -1:  # Down
        glRotatef(-90, 0, 0, 1)

    glutSolidSphere(CELL_SIZE * 0.4, 12, 12)

    # Eyes - white with black pupils
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(CELL_SIZE * 0.25, CELL_SIZE * 0.15, CELL_SIZE * 0.15)
    glutSolidSphere(CELL_SIZE * 0.08, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(CELL_SIZE * 0.25, -CELL_SIZE * 0.15, CELL_SIZE * 0.15)
    glutSolidSphere(CELL_SIZE * 0.08, 8, 8)
    glPopMatrix()

    # Pupils - kalo dots
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(CELL_SIZE * 0.32, CELL_SIZE * 0.15, CELL_SIZE * 0.15)
    glutSolidSphere(CELL_SIZE * 0.04, 6, 6)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(CELL_SIZE * 0.32, -CELL_SIZE * 0.15, CELL_SIZE * 0.15)
    glutSolidSphere(CELL_SIZE * 0.04, 6, 6)
    glPopMatrix()

    glPopMatrix()

    # Body segments - head theke ektu dim
    body_color = (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)

    if special_effects["invincibility"]:
        glColor3f(0.8, 0.8, 0.0)
    elif special_effects["speed_boost"]:
        glColor3f(0.0, 0.8, 0.8)
    elif special_effects["double_points"]:
        glColor3f(0.8, 0.4, 0.8)
    else:
        glColor3f(*body_color)

    for i in range(1, len(snake_positions)):
        body_x, body_y = snake_positions[i]
        world_x, world_y = convert_world_coords(body_x, body_y)

        glPushMatrix()
        glTranslatef(world_x, world_y, HALF_CELL * 0.8)
        glutSolidSphere(CELL_SIZE * 0.35, 10, 10)
        glPopMatrix()

def draw_food():
    # Normal food - apple er moto banalam with stem
    if not food_position:
        return

    food_x, food_y = food_position
    world_x, world_y = convert_world_coords(food_x, food_y)

    glPushMatrix()
    glTranslatef(world_x, world_y, HALF_CELL)

    # Apple body - lal
    glColor3f(1.0, 0.2, 0.2)
    glutSolidSphere(CELL_SIZE * 0.3, 12, 12)

    # Stem - brown color
    glColor3f(0.4, 0.2, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, CELL_SIZE * 0.25)
    glutSolidCylinder(CELL_SIZE * 0.05, CELL_SIZE * 0.15, 6, 2)
    glPopMatrix()

    glPopMatrix()

def draw_special_food():
    # Special food - rotating star with glow effect
    if not special_food_position:
        return

    food_x, food_y = special_food_position
    world_x, world_y = convert_world_coords(food_x, food_y)

    glPushMatrix()
    glTranslatef(world_x, world_y, HALF_CELL)

    # Rotating animation - time based
    rotation_angle = (time.time() * 60) % 360
    glRotatef(rotation_angle, 0, 0, 1)

    # Glow effect - pulsing brightness
    glow_intensity = 0.5 + 0.5 * math.sin(time.time() * 4)

    # Different colors for different power-ups
    if special_food_type == "SPEED":
        glColor3f(0.0, glow_intensity, 1.0)
    elif special_food_type == "DOUBLE_POINTS":
        glColor3f(1.0, glow_intensity, 0.0)
    elif special_food_type == "INVINCIBILITY":
        glColor3f(1.0, 1.0, glow_intensity)

    # 5-pointed star shape - manually draw korlam
    glBegin(GL_TRIANGLES)
    for i in range(10):
        angle1 = (i * 36) * math.pi / 180
        angle2 = ((i + 1) * 36) * math.pi / 180

        radius1 = CELL_SIZE * 0.4 if i % 2 == 0 else CELL_SIZE * 0.2
        radius2 = CELL_SIZE * 0.4 if (i + 1) % 2 == 0 else CELL_SIZE * 0.2

        glVertex3f(0, 0, 0)
        glVertex3f(radius1 * math.cos(angle1), radius1 * math.sin(angle1), 0)
        glVertex3f(radius2 * math.cos(angle2), radius2 * math.sin(angle2), 0)
    glEnd()

    glPopMatrix()

def draw_obstacles():
    # Gray cubes - avoid korte hobe
    glColor3f(0.4, 0.4, 0.4)

    for obs_x, obs_y in obstacles:
        world_x, world_y = convert_world_coords(obs_x, obs_y)

        glPushMatrix()
        glTranslatef(world_x, world_y, HALF_CELL)
        glutSolidCube(CELL_SIZE * 0.8)
        glPopMatrix()

def draw_bombs():
    # Bombs - black sphere with red fuse
    for bomb_x, bomb_y in bombs:
        world_x, world_y = convert_world_coords(bomb_x, bomb_y)

        glPushMatrix()
        glTranslatef(world_x, world_y, HALF_CELL)

        # Bomb body - kala
        glColor3f(0.1, 0.1, 0.1)
        glutSolidSphere(CELL_SIZE * 0.35, 12, 12)

        # Fuse - lal cylinder
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 0, CELL_SIZE * 0.3)
        glutSolidCylinder(CELL_SIZE * 0.05, CELL_SIZE * 0.2, 6, 2)
        glPopMatrix()

        glPopMatrix()

def generate_food():
    # Random position e food spawn - valid location khuje ber kore
    global food_position
    valid_positions = get_valid_positions([special_food_position] if special_food_position else [])
    if valid_positions:
        food_position = random.choice(valid_positions)
    else:
        food_position = None

def generate_special_food():
    # Special power-up food generate
    global special_food_position, special_food_type
    valid_positions = get_valid_positions([food_position] if food_position else [])
    if valid_positions:
        special_food_position = random.choice(valid_positions)
        special_food_type = random.choice(["SPEED", "DOUBLE_POINTS", "INVINCIBILITY"])
    else:
        special_food_position = None

def generate_obstacles():
    # Difficulty onujayi obstacle count
    global obstacles
    obstacles = []

    if game_mode == "QUICK_PLAY":
        obstacle_count = {"NORMAL": 2, "HARD": 3, "PUNISHER": 5}[difficulty]
    else:
        obstacle_count = {"NORMAL": 3, "HARD": 6, "PUNISHER": 10}[difficulty]

    # Snake ar food er position avoid kore
    exclude_positions = snake_positions.copy()
    if food_position is not None:
        exclude_positions.append(food_position)
    if special_food_position is not None:
        exclude_positions.append(special_food_position)

    valid_positions = get_valid_positions(exclude_positions)

    for _ in range(min(obstacle_count, len(valid_positions))):
        if valid_positions:
            pos = random.choice(valid_positions)
            obstacles.append(pos)
            valid_positions.remove(pos)

def generate_bombs():
    # Bombs are more dangerous than obstacles
    global bombs
    bombs = []

    if game_mode == "QUICK_PLAY":
        bomb_count = {"NORMAL": 0, "HARD": 1, "PUNISHER": 2}[difficulty]
    else:
        bomb_count = {"NORMAL": 1, "HARD": 2, "PUNISHER": 4}[difficulty]

    exclude_positions = snake_positions.copy() + obstacles.copy()
    if food_position is not None:
        exclude_positions.append(food_position)
    if special_food_position is not None:
        exclude_positions.append(special_food_position)

    valid_positions = get_valid_positions(exclude_positions)

    for _ in range(min(bomb_count, len(valid_positions))):
        if valid_positions:
            pos = random.choice(valid_positions)
            bombs.append(pos)
            valid_positions.remove(pos)

def move_snake():
    # Main game logic - snake movement ar collision detection
    global snake_positions, score, food_eaten, level, game_state, fruits_collected
    global special_food_position, special_food_type

    if game_state != "PLAYING":
        return

    head_x, head_y = snake_positions[0]
    dir_x, dir_y = snake_direction

    new_head_x = head_x + dir_x
    new_head_y = head_y + dir_y

    # Borderless mode e wall cross korle ulta dik theke ashbe
    if game_mode != "BORDERLESS":
        if new_head_x < 0 or new_head_x >= GRID_SIZE or new_head_y < 0 or new_head_y >= GRID_SIZE:
            game_over()
            return
    else:
        new_head_x, new_head_y = normalize_position(new_head_x, new_head_y)

    new_head = (new_head_x, new_head_y)

    # Collision detection - cheat na thakle
    if not (cheat_invincibility or special_effects["invincibility"]):
        # Self collision
        if new_head in snake_positions:
            game_over()
            return

        # Bomb collision - immediate death
        if new_head in bombs:
            game_over()
            return

        # Obstacle collision
        if new_head in obstacles:
            if cheat_mode:
                obstacles.remove(new_head)  # Cheat mode e obstacle hataiye dey
            else:
                game_over()
                return

    snake_positions.insert(0, new_head)

    ate_food = False

    # Normal food khele
    if new_head == food_position:
        points = 2 if special_effects["double_points"] else 1
        score += points
        food_eaten += 1
        fruits_collected += 1
        ate_food = True
        generate_food()

        # Certain interval e special food appear korbe
        special_food_interval = 3 if game_mode == "QUICK_PLAY" else 5
        if food_eaten % special_food_interval == 0:
            generate_special_food()

    # Special food khele
    elif new_head == special_food_position:
        points = 4 if special_effects["double_points"] else 2
        score += points
        fruits_collected += 1
        ate_food = True

        # Power-up activate
        special_effects[special_food_type.lower()] = True
        special_effects["effect_start_time"] = time.time()

        if special_food_type == "SPEED":
            set_snake_speed()

        special_food_position = None
        special_food_type = None

    # Quick play mode e snake grow hoy na - different mechanic
    if game_mode == "QUICK_PLAY":
        if not ate_food:
            snake_positions.pop()
    else:
        if not ate_food:
            snake_positions.pop()

    # Level progression - survival mode e
    if game_mode != "QUICK_PLAY" and score >= level * 10:
        level += 1
        generate_obstacles()
        generate_bombs()
        update_atmosphere()

def update_special_effects():
    # Power-up effects er duration track kore
    global special_effects

    current_time = time.time()

    for effect in ["speed_boost", "double_points", "invincibility"]:
        if special_effects[effect]:
            elapsed = current_time - special_effects["effect_start_time"]
            if elapsed >= special_effects["effect_duration"]:
                special_effects[effect] = False

                # Speed boost shesh hole normal speed e fire ashbe
                if effect == "speed_boost":
                    set_snake_speed()

def get_valid_positions(exclude_positions=None):
    # Snake ar obstacles chara jekhanei food spawn korte parbo
    if exclude_positions is None:
        exclude_positions = []

    valid_positions = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pos = (x, y)
            if pos not in snake_positions and pos not in exclude_positions:
                if pos not in obstacles and pos not in bombs:
                    valid_positions.append(pos)
    return valid_positions