# 贪吃蛇游戏 (Snake Game)

一个使用 Python 和 Pygame 开发的智能贪吃蛇游戏，包含AI自动测试功能。
(A smart Snake Game developed with Python and Pygame, featuring AI testing capabilities.)

## 游戏特性 (Game Features)

- 简单易上手的操控方式 (Simple and intuitive controls)
- 清晰的得分显示 (Clear score display)
- 流畅的游戏体验 (Smooth gaming experience)
- 中文界面 (Chinese language interface)
- 精确的碰撞检测 (Precise collision detection)
- AI自动测试模式 (AI Testing Mode)
- A*寻路算法 (A* Pathfinding Algorithm)
- 智能避障系统 (Smart Obstacle Avoidance)

## 环境设置 (Environment Setup)

### 激活虚拟环境 (Activate Virtual Environment)

#### Windows 命令提示符 (Windows Command Prompt):
```
snake_env\Scripts\activate.bat
```

#### Windows PowerShell:
```
snake_env\Scripts\Activate.ps1
```

### 安装依赖 (Install Dependencies)
虚拟环境激活后，安装必要的包 (After activating the virtual environment, install the necessary packages):
```
pip install pygame
```

## 运行游戏 (Run the Game)

### 普通模式 (Normal Mode)
```
python 贪吃蛇.py
```

### AI测试模式 (AI Test Mode)
运行单次测试 (Run single test):
```
python run_ai_test.py
```

运行多次测试 (Run multiple tests):
```
python run_ai_test.py <次数>
```
例如运行5次测试 (For example, run 5 tests):
```
python run_ai_test.py 5
```

## 游戏控制 (Game Controls)

### 玩家模式 (Player Mode)
- 空格键：开始游戏 (Space: Start game)
- 上下左右箭头键：控制蛇的移动方向 (Arrow keys: Control snake movement)
- 游戏结束后按 'C' 重新开始，按 'Q' 退出游戏 (After game over, press 'C' to restart or 'Q' to quit)
- 关卡过渡界面按空格键继续 (Press Space to continue at level transition screens)

### AI测试模式 (AI Test Mode)
- AI会自动控制蛇的移动 (AI automatically controls snake movement)
- 使用A*算法寻找最优路径 (Uses A* algorithm to find optimal path)
- 智能避障和空间评估 (Smart obstacle avoidance and space evaluation)
- 自动记录测试结果 (Automatically records test results)

## 游戏规则 (Game Rules)
- 使用方向键控制蛇移动收集红色食物 (Use arrow keys to control the snake and collect red food)
- 每吃一个食物，蛇身增长一节，得分加1 (Snake grows longer and score increases by 1 with each food eaten)
- 撞到墙壁或自身则游戏结束 (Game ends if snake hits the wall or itself)
- 游戏结束后可以按 C 重新开始，或按 Q 退出 (After game over, press C to restart or Q to quit)

## 技术实现 (Technical Implementation)

### 基础功能 (Basic Features)
- 使用 Pygame 库进行图形和游戏机制实现 (Uses Pygame for graphics and game mechanics)
- 使用 simhei.ttf 字体支持中文界面 (Uses simhei.ttf font for Chinese interface)
- 支持以可执行文件形式运行 (Supports running as executable)
- 精确的位置计算和碰撞检测 (Precise position calculation and collision detection)
- 流畅的动画效果 (Smooth animation effects)

### AI系统 (AI System)
- A*寻路算法实现最优路径规划 (A* algorithm for optimal path planning)
- 智能空间评估系统 (Intelligent space evaluation system)
- 预测性避障功能 (Predictive obstacle avoidance)
- 自动化测试框架 (Automated testing framework)

## 创建可执行文件 (Create Executable)
游戏提供了简单的打包脚本，可以一键生成可执行文件 (The game provides a simple packaging script for one-click executable generation):
```
python build.py
```

打包完成后，在 dist/贪吃蛇/ 目录下可以找到以下文件 (After packaging, you can find the following files in the dist/贪吃蛇/ directory):
- 贪吃蛇.exe (主游戏程序 Main game program)
- snake_test.py (AI测试系统 AI test system)
- run_ai_test.py (AI测试运行器 AI test runner)
- simhei.ttf (字体文件 Font file)

## 项目结构 (Project Structure)
```
├── 贪吃蛇.py          # 主游戏文件 (Main game file)
├── snake_test.py     # AI测试系统 (AI test system)
├── run_ai_test.py    # AI测试运行器 (AI test runner)
├── simhei.ttf        # 中文字体文件 (Chinese font file)
└── README.md         # 项目说明文档 (Project documentation)
```

## AI测试结果分析 (AI Test Results Analysis)
AI测试模式会记录以下数据：
- 移动次数 (Number of moves)
- 最终得分 (Final score)
- 游戏状态 (Game state)
- 路径规划效率 (Path planning efficiency)
- 避障成功率 (Obstacle avoidance success rate)

## 开发计划 (Development Plan)
- [ ] 添加更多测试场景 (Add more test scenarios)
- [ ] 优化路径规划算法 (Optimize path planning algorithm)
- [ ] 实现深度学习模型 (Implement deep learning model)
- [ ] 添加游戏录像功能 (Add game recording feature)
- [ ] 支持多种AI策略 (Support multiple AI strategies)