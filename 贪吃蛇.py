import pygame
import time
import random
import sys
import os
import math

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

def update_snake_state(snake_list, food_pos, obstacles, score, game_over):
    """更新AI使用的游戏状态"""
    from snake_test import update_game_state
    update_game_state(snake_list, food_pos, obstacles, score, game_over)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

# Game states
MENU = 'menu'
PLAYING = 'playing'
PAUSED = 'paused'
GAME_OVER = 'game_over'
TUTORIAL = 'tutorial'

# Set display
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇 - Snake Game')

# Set clock
clock = pygame.time.Clock()
SNAKE_SPEED = 8  # Base speed

# Game settings
LEVEL_SCORE_THRESHOLD = 5  # Score needed to advance to next level
SPEED_INCREMENT = 2  # How much to increase speed per level
MAX_LEVEL = 5  # Maximum level
STARTING_SPEED = 8
HIGH_SCORE_FILE = "highscore.txt"

# Difficulty settings
DIFFICULTIES = {
    "简单": {"speed": 6, "obstacles": False, "wall_collision": False},
    "普通": {"speed": 8, "obstacles": True, "wall_collision": True},
    "困难": {"speed": 10, "obstacles": True, "wall_collision": True}
}

# Animation settings
ANIMATION_SPEED = 5
PARTICLE_LIFETIME = 20
PARTICLE_COLORS = [YELLOW, ORANGE, RED]

# Power-up settings
POWERUP_CHANCE = 0.1  # 10% chance to spawn a power-up
POWERUP_DURATION = 10  # seconds
POWERUP_TYPES = ["speed", "invincible", "double_points"]

# Sound effects
try:
    EAT_SOUND = pygame.mixer.Sound("eat.wav")
    LEVEL_UP_SOUND = pygame.mixer.Sound("levelup.wav")
    GAME_OVER_SOUND = pygame.mixer.Sound("gameover.wav")
except:
    EAT_SOUND = None
    LEVEL_UP_SOUND = None
    GAME_OVER_SOUND = None

# Font for score
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
font_path = os.path.join(base_path, "simhei.ttf")
font_style = pygame.font.Font(font_path, 30)
score_font = pygame.font.Font(font_path, 35)


def display_score(score, level, high_score):
    """Display the current score, level and high score on the screen"""
    # Score
    score_value = score_font.render("得分: " + str(score), True, BLACK)
    game_display.blit(score_value, [10, 10])
    
    # Level with color change based on level
    level_color = (min(255, 50 + 50 * level), max(0, 255 - 30 * level), 0)
    level_value = score_font.render("关卡: " + str(level), True, level_color)
    game_display.blit(level_value, [WINDOW_WIDTH - 150, 10])
    
    # High Score
    high_score_value = score_font.render("最高分: " + str(high_score), True, RED)
    game_display.blit(high_score_value, [10, 50])


def draw_snake(block_size, snake_list):
    """Draw the snake on the screen with gradient color and eyes"""
    for i, segment in enumerate(snake_list):
        # Gradient color from dark green (tail) to bright green (head)
        color_factor = i / max(len(snake_list), 1)
        segment_color = (
            int(DARK_GREEN[0] + (GREEN[0] - DARK_GREEN[0]) * color_factor),
            int(DARK_GREEN[1] + (GREEN[1] - DARK_GREEN[1]) * color_factor),
            int(DARK_GREEN[2] + (GREEN[2] - DARK_GREEN[2]) * color_factor)
        )
        
        # Draw snake segment with rounded corners
        pygame.draw.rect(game_display, segment_color, 
                        [segment[0], segment[1], block_size, block_size], 0, 3)
        
        # Draw eyes on the head
        if i == len(snake_list) - 1:  # This is the head
            eye_radius = block_size // 6
            # Left eye
            pygame.draw.circle(game_display, WHITE, 
                             (segment[0] + block_size//3, segment[1] + block_size//3), 
                             eye_radius)
            pygame.draw.circle(game_display, BLACK, 
                             (segment[0] + block_size//3, segment[1] + block_size//3), 
                             eye_radius//2)
            # Right eye
            pygame.draw.circle(game_display, WHITE, 
                             (segment[0] + 2*block_size//3, segment[1] + block_size//3), 
                             eye_radius)
            pygame.draw.circle(game_display, BLACK, 
                             (segment[0] + 2*block_size//3, segment[1] + block_size//3), 
                             eye_radius//2)


def message(msg, color, y_offset=0):
    """Display a message on the screen"""
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + y_offset))
    game_display.blit(mesg, mesg_rect)


def generate_food(obstacles=None):
    """Generate a random position for food that's not inside an obstacle"""
    if obstacles is None:
        obstacles = []
    
    while True:
        food_x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        
        # Check if the food position overlaps with any obstacle
        position_valid = True
        for obstacle in obstacles:
            if food_x == obstacle[0] and food_y == obstacle[1]:
                position_valid = False
                break
        
        if position_valid:
            return food_x, food_y


def generate_obstacles(level, snake_pos=None):
    """Generate obstacles based on the current level"""
    obstacles = []
    
    if level <= 1:
        return obstacles  # No obstacles at level 1
    
    # Number of obstacles increases with level
    num_obstacles = (level - 1) * 3
    
    # Ensure snake's starting position is safe
    safe_zone = []
    if snake_pos:
        safe_zone = [snake_pos[0], snake_pos[1]]
    
    for _ in range(num_obstacles):
        while True:
            obs_x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            obs_y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            
            # Make sure obstacle isn't on the snake or in the safe zone
            if (not safe_zone or (obs_x != safe_zone[0] or obs_y != safe_zone[1])):
                obstacles.append((obs_x, obs_y))
                break
                
    return obstacles

def show_level_screen(level):
    """Show level transition screen"""
    game_display.fill(WHITE)
    message(f"恭喜! 进入关卡 {level}", GREEN)
    message("按空格键继续", BLACK, 30)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

def load_high_score():
    """Load the high score from file"""
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    """Save the high score to file"""
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except:
        pass

def create_particle_effect(x, y, color):
    """Create particle effect at given position"""
    particles = []
    for _ in range(10):
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(2, 5)
        particle = {
            'x': x,
            'y': y,
            'dx': math.cos(angle) * speed,
            'dy': math.sin(angle) * speed,
            'lifetime': PARTICLE_LIFETIME,
            'color': color
        }
        particles.append(particle)
    return particles

def update_particles(particles):
    """Update particle positions and lifetimes"""
    alive_particles = []
    for p in particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['lifetime'] -= 1
        if p['lifetime'] > 0:
            alive_particles.append(p)
    return alive_particles

def draw_particles(particles):
    """Draw particles on screen"""
    for p in particles:
        alpha = int(255 * (p['lifetime'] / PARTICLE_LIFETIME))
        color = p['color'] + (alpha,)
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (2, 2), 2)
        game_display.blit(s, (int(p['x']), int(p['y'])))

def show_tutorial():
    """Display game tutorial"""
    tutorial_steps = [
        ("欢迎来到贪吃蛇游戏教程!", "使用方向键控制蛇的移动", GREEN),
        ("游戏目标", "吃掉红色食物来增长蛇的长度", RED),
        ("注意事项", "避免撞到墙壁、障碍物或自己", BLUE),
        ("特殊物品", "黄色物品是特殊能力, 可以获得临时增益", YELLOW),
        ("游戏控制", "空格键: 暂停游戏\nP键: 暂停\nQ键: 退出", ORANGE)
    ]
    
    for title, desc, color in tutorial_steps:
        game_display.fill(WHITE)
        message(title, color, -50)
        message(desc, BLACK, 0)
        message("按空格键继续...", GREY, 50)
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            clock.tick(5)

def draw_menu():
    """Draw the main menu"""
    game_display.fill(WHITE)
    message("贪吃蛇", GREEN, -100)
    message("1. 开始游戏", BLACK, -30)
    message("2. 教程", BLACK, 0)
    message("3. 选择难度", BLACK, 30)
    message("4. 退出", BLACK, 60)
    pygame.display.update()

def choose_difficulty():
    """Let player choose difficulty"""
    game_display.fill(WHITE)
    message("选择难度", BLUE, -50)
    message("1. 简单", GREEN, -20)
    message("2. 普通", YELLOW, 10)
    message("3. 困难", RED, 40)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "简单"
                elif event.key == pygame.K_2:
                    return "普通"
                elif event.key == pygame.K_3:
                    return "困难"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

def spawn_powerup():
    """Spawn a power-up item"""
    if random.random() < POWERUP_CHANCE:
        power_x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        power_y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        power_type = random.choice(POWERUP_TYPES)
        return power_x, power_y, power_type
    return None

def apply_powerup(power_type, current_speed, score_multiplier):
    """Apply power-up effects"""
    if power_type == "speed":
        return current_speed * 0.75, score_multiplier
    elif power_type == "invincible":
        return current_speed, score_multiplier
    elif power_type == "double_points":
        return current_speed, score_multiplier * 2
    return current_speed, score_multiplier

def game_loop(ai_mode=False):
    """Main game loop"""
    game_state = MENU
    high_score = load_high_score()
    
    # 创建全局游戏状态字典供AI使用
    global game_status
    game_status = {
        'snake_list': [],
        'food_position': None,
        'obstacles': [],
        'score': 0,
        'game_over': False
    }
    
    # 如果是AI模式，跳过主菜单并初始化AI
    if ai_mode:
        from snake_test import SnakeAI
        ai = SnakeAI()
        game_start = True  # 立即开始游戏
        print("AI模式已启动")
    # Game variables
    game_over = False
    game_close = False
    game_start = False
    game_paused = False
    current_level = 1
    level_changed = False
    
    # Choose difficulty
    difficulty = "普通"  # default difficulty
    difficulty_settings = DIFFICULTIES[difficulty]
    
    # Particle effects
    particles = []
    
    # Power-up
    active_powerup = None
    powerup_timer = 0
    powerup_position = None
    score_multiplier = 1
    
    # Initial snake position and movement
    x = int(WINDOW_WIDTH / 2)  # 确保位置是整数
    y = int(WINDOW_HEIGHT / 2)
    x_change = 0
    y_change = 0
    
    # Snake body
    snake_list = [(x, y)]  # 使用元组初始化蛇头位置
    snake_length = 1
    
    # Obstacles
    obstacles = [(obs[0], obs[1]) for obs in generate_obstacles(current_level, (x, y))]
    
    print(f"游戏初始化：蛇头位置=({x}, {y})")
    
    # Initial food position
    food_x, food_y = generate_food(obstacles)
    
    # Current speed based on level
    current_speed = SNAKE_SPEED + (current_level - 1) * SPEED_INCREMENT
    
    # Start screen
    if not ai_mode:
        while not game_start and not game_over:
            game_display.fill(WHITE)
            message("欢迎来到贪吃蛇游戏!", GREEN)
            message("按空格键开始游戏", BLACK, 30)
            message(f"当前关卡: {current_level}", BLUE, 60)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_start = True
                    elif event.key == pygame.K_q:
                        game_over = True
    else:
        game_start = True  # AI模式直接开始游戏
    
    # Main game loop
    while not game_over and game_start:
        
        # Game over screen
        while game_close:
            game_display.fill(WHITE)
            message("游戏结束! 按Q退出或按C重新开始", RED)
            display_score(snake_length - 1, current_level, high_score)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                elif event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if not ai_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0
                    
        # AI控制
        if ai_mode:
            ai.update_state(game_status)
            direction = ai.decide_move()
            if direction == "LEFT" and x_change == 0:
                x_change = -BLOCK_SIZE
                y_change = 0
            elif direction == "RIGHT" and x_change == 0:
                x_change = BLOCK_SIZE
                y_change = 0
            elif direction == "UP" and y_change == 0:
                y_change = -BLOCK_SIZE
                x_change = 0
            elif direction == "DOWN" and y_change == 0:
                y_change = BLOCK_SIZE
                x_change = 0
        
        # Check for boundary collision
        if x >= WINDOW_WIDTH or x < 0 or y >= WINDOW_HEIGHT or y < 0:
            game_close = True
        
        # Update snake position
        x += x_change
        y += y_change
        
        # Draw game elements
        game_display.fill(WHITE)
        
        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(game_display, BLUE, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
            
        pygame.draw.rect(game_display, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        # Add new segment to snake
        x = int(x)  # 确保位置是整数
        y = int(y)
        snake_head = (x, y)  # 使用元组而不是列表
        snake_list.append(snake_head)
        
        # Remove extra segments if snake didn't grow
        if len(snake_list) > snake_length:
            del snake_list[0]
            
        if ai_mode:
            print(f"蛇移动：位置=({x}, {y}), 长度={len(snake_list)}")
        
        # Check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
                
        # Update game status
        game_status['snake_list'] = snake_list.copy()
        game_status['food_position'] = (food_x, food_y)
        game_status['obstacles'] = obstacles.copy()
        game_status['score'] = snake_length - 1
        game_status['game_over'] = game_close
        
        # Draw snake and display score
        draw_snake(BLOCK_SIZE, snake_list)
        display_score(snake_length - 1, current_level, high_score)
        
        pygame.display.update()
        
        # Check if snake ate food
        if x == food_x and y == food_y:
            food_x, food_y = generate_food(obstacles)
            snake_length += 1
            
            # Check if player should advance to next level
            score = snake_length - 1
            if score % LEVEL_SCORE_THRESHOLD == 0 and current_level < MAX_LEVEL:
                current_level += 1
                level_changed = True
                current_speed = SNAKE_SPEED + (current_level - 1) * SPEED_INCREMENT
                
        # Check for collision with obstacles
        for obs in obstacles:
            if x == obs[0] and y == obs[1]:
                game_close = True
        
        # Show level transition screen if level changed
        if level_changed:
            show_level_screen(current_level)
            obstacles = generate_obstacles(current_level)
            food_x, food_y = generate_food(obstacles)
            level_changed = False
        
        # Control game speed
        clock.tick(current_speed)
    
    # Quit pygame
    pygame.quit()
    quit()

if __name__ == "__main__":
    # 解析命令行参数
    import sys
    ai_mode = "--ai" in sys.argv
    game_loop(ai_mode)


# Start the game
if __name__ == "__main__":
    game_loop()