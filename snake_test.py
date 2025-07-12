import pygame
import time
from 贪吃蛇 import *
import math
import random

# 全局游戏状态
game_state = {
    'snake_list': [],
    'food_position': None,
    'obstacles': [],
    'score': 0,
    'game_over': False
}

def update_game_state(snake_list, food_pos, obstacles, score, game_over):
    """更新全局游戏状态"""
    global game_state
    game_state = {
        'snake_list': [tuple(map(int, pos)) for pos in snake_list] if snake_list else [],
        'food_position': tuple(map(int, food_pos)) if food_pos else None,
        'obstacles': [tuple(map(int, pos)) for pos in obstacles] if obstacles else [],
        'score': score,
        'game_over': game_over
    }
    print(f"状态更新：蛇头位置={game_state['snake_list'][-1] if game_state['snake_list'] else None}, 食物位置={game_state['food_position']}")

def get_game_state():
    """获取当前游戏状态"""
    return game_state

class SnakeAI:
    def __init__(self, game_state=None):
        """初始化AI控制器"""
        self.game_state = game_state if game_state else {}
        self.block_size = BLOCK_SIZE
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        
    def update_state(self, state):
        """更新游戏状态"""
        self.game_state = state
        
    def will_collide(self, x, y, obstacles):
        """检查是否会发生碰撞"""
        # 边界检查
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
            
        # 障碍物检查
        if (x, y) in obstacles:
            return True
            
        # 检查是否会撞到蛇身
        if 'snake_list' in self.game_state:
            snake_body = self.game_state['snake_list'][:-1]  # 不包括蛇头
            if (x, y) in snake_body:
                return True
                
        return False
        
    def manhattan_distance(self, p1, p2):
        """计算曼哈顿距离"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
    def get_neighbors(self, pos, obstacles):
        """获取邻近的有效位置"""
        x, y = pos
        neighbors = []
        for dx, dy in [(0, self.block_size), (0, -self.block_size),
                       (self.block_size, 0), (-self.block_size, 0)]:
            new_x = x + dx
            new_y = y + dy
            if not self.will_collide(new_x, new_y, obstacles):
                neighbors.append((new_x, new_y))
        return neighbors
        
    def find_path(self, start, goal, obstacles):
        """使用A*算法寻找路径"""
        if not start or not goal:
            return None
            
        # 确保起点和终点是元组
        start = tuple(start) if isinstance(start, list) else start
        goal = tuple(goal) if isinstance(goal, list) else goal
        obstacles = [tuple(pos) if isinstance(pos, list) else pos for pos in obstacles]
            
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}
        
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]
                
            open_set.remove(current)
            
            for neighbor in self.get_neighbors(current, obstacles):
                tentative_g = g_score[current] + self.block_size
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.manhattan_distance(neighbor, goal)
                    open_set.add(neighbor)
        
        return None
        
    def get_direction(self, current_pos, target_pos):
        """获取从当前位置到目标位置的方向"""
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        if dx > 0: return "RIGHT"
        if dx < 0: return "LEFT"
        if dy > 0: return "DOWN"
        if dy < 0: return "UP"
        return None
        
    def get_safe_move(self, head, obstacles):
        """获取一个安全的移动方向，优先选择空间较大的方向"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        moves = {"UP": (0, -self.block_size),
                "DOWN": (0, self.block_size),
                "LEFT": (-self.block_size, 0),
                "RIGHT": (self.block_size, 0)}
        
        # 评估每个方向的安全度
        safe_moves = []
        for direction in directions:
            dx, dy = moves[direction]
            new_x = head[0] + dx
            new_y = head[1] + dy
            if not self.will_collide(new_x, new_y, obstacles):
                # 计算这个方向的空间大小
                space = self._count_free_space((new_x, new_y), obstacles)
                safe_moves.append((direction, space))
                
        if not safe_moves:
            return None
            
        # 选择空间最大的方向
        safe_moves.sort(key=lambda x: x[1], reverse=True)
        return safe_moves[0][0]
        
    def _count_free_space(self, start, obstacles, max_depth=5):
        """计算某个位置可以到达的空闲格子数量"""
        visited = {start}
        to_visit = {start}
        depth = 0
        
        while to_visit and depth < max_depth:
            next_visit = set()
            for pos in to_visit:
                for dx, dy in [(0, self.block_size), (0, -self.block_size),
                              (self.block_size, 0), (-self.block_size, 0)]:
                    new_pos = (pos[0] + dx, pos[1] + dy)
                    if (new_pos not in visited and 
                        not self.will_collide(new_pos[0], new_pos[1], obstacles)):
                        visited.add(new_pos)
                        next_visit.add(new_pos)
            to_visit = next_visit
            depth += 1
            
        return len(visited)
        
    def decide_move(self):
        """决定下一步移动"""
        if not self.game_state or 'snake_list' not in self.game_state:
            print("游戏状态无效")
            return None
            
        if not self.game_state['snake_list']:
            print("蛇列表为空")
            return None
            
        snake_head = self.game_state['snake_list'][-1]
        food_pos = self.game_state['food_position']
        obstacles = self.game_state.get('obstacles', [])
        
        print(f"AI决策：蛇头={snake_head}, 食物={food_pos}, 障碍数量={len(obstacles)}")
        
        # 寻找到食物的路径
        path = self.find_path(snake_head, food_pos, obstacles)
        
        if path and len(path) > 1:
            # 如果找到路径，选择下一个位置
            next_pos = path[1]
            return self.get_direction(snake_head, next_pos)
        else:
            # 如果找不到路径，选择一个安全的方向
            return self.get_safe_move(snake_head, obstacles)

# 键盘映射
KEY_MAP = {"UP": pygame.K_UP, "DOWN": pygame.K_DOWN, 
           "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT}

def simulate_keypress(direction):
    """模拟按键事件"""
    if direction in KEY_MAP:
        key = KEY_MAP[direction]
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': key}))
        return key
    return None

def run_ai_test(max_moves=1000, visualize=True):
    """运行AI测试"""
    global game_state
    if not game_state or 'snake_list' not in game_state:
        print("游戏状态不完整")
        return False
        
    ai = SnakeAI()
    moves_made = 0
    last_score = game_state['score']
    no_progress_count = 0
    
    while moves_made < max_moves and not game_state['game_over']:
        ai.update_state(get_game_state())
        
        # 获取AI的决策
        direction = ai.decide_move()
        
        if not direction:
            print("AI无法找到有效的移动方向")
            break
            
        # 执行移动
        simulate_keypress(direction)
        
        # 检查得分是否增加
        current_score = game_state['score']
        if current_score > last_score:
            last_score = current_score
            no_progress_count = 0
        else:
            no_progress_count += 1
            
        # 如果长时间没有进展，可能陷入循环
        if no_progress_count > 100:
            print("AI可能陷入循环，终止测试")
            break
            
        moves_made += 1
        
        # 如果需要可视化，添加延迟
        if visualize:
            time.sleep(0.1)
            
    test_results = {
        'moves': moves_made,
        'final_score': game_state['score'],
        'game_over': game_state['game_over']
    }
    
    print(f"测试结束: 移动次数={moves_made}, 最终得分={game_state['score']}")
    return test_results
