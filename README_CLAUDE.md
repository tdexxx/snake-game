# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Virtual Environment Setup
The project uses a Python virtual environment located in `snake_env/`. Activate it before development:

**Windows Command Prompt:**
```
snake_env\Scripts\activate.bat
```

**Windows PowerShell:**
```
snake_env\Scripts\Activate.ps1
```

### Install Dependencies
After activating the virtual environment:
```
pip install pygame
```

### Running the Game

**Normal Game Mode:**
```
python 贪吃蛇.py
```

**AI Test Mode (single test):**
```
python run_ai_test.py
```

**AI Test Mode (multiple tests):**
```
python run_ai_test.py <number_of_tests>
```
Example: `python run_ai_test.py 5`

**AI Mode via main game (alternative):**
```
python 贪吃蛇.py --ai
```

### Building Executable
```
python build.py
```
This creates a distributable executable in `dist/贪吃蛇/` with all necessary files.

## Code Architecture

### Main Game Architecture (贪吃蛇.py)
- **Game Engine**: Built on pygame with state management for menu, playing, paused, game_over states
- **Core Game Loop**: `game_loop()` function handles all game mechanics including AI integration
- **AI Integration**: The game can run in AI mode using the `--ai` flag or `ai_mode=True` parameter
- **Global State Management**: Uses `game_status` dictionary to share state with AI system

### AI System (snake_test.py)
- **SnakeAI Class**: Implements intelligent snake control using A* pathfinding algorithm
- **State Management**: `update_game_state()` and `get_game_state()` functions for communication with main game
- **Pathfinding**: A* algorithm with Manhattan distance heuristic for optimal food targeting
- **Safety System**: Collision detection and safe move selection when direct path is blocked
- **Space Evaluation**: `_count_free_space()` method prevents AI from getting trapped

### Key Game Components
- **Snake Rendering**: Gradient coloring from tail to head with eyes on head segment
- **Collision Detection**: Precise boundary, obstacle, and self-collision checking
- **Level System**: Progressive difficulty with speed increases and obstacle generation
- **Obstacle Generation**: `generate_obstacles()` creates level-appropriate challenges
- **Food System**: `generate_food()` ensures food spawns in valid locations

### AI Decision Making Flow
1. AI receives game state via `update_state()`
2. `decide_move()` attempts A* pathfinding to food
3. If path found, moves toward next position in path
4. If no path available, uses `get_safe_move()` to find safest direction
5. Safe move selection prioritizes areas with most free space

### Build System
- **PyInstaller Integration**: Uses PyInstaller 5.13.2 for executable generation
- **Asset Management**: Automatically includes Chinese font file (simhei.ttf)
- **Multi-file Distribution**: Creates package with main exe, AI test files, and assets
- **Spec File**: Pre-configured PyInstaller specification for consistent builds

## File Organization

### Core Files
- `贪吃蛇.py` - Main game executable with pygame-based snake game
- `snake_test.py` - AI controller with A* pathfinding and safety algorithms
- `run_ai_test.py` - AI test runner for automated testing
- `build.py` - Build script for executable generation
- `simhei.ttf` - Chinese font file for game interface

### Build Artifacts
- `贪吃蛇.spec` - PyInstaller specification file
- `build/` - Temporary build files
- `dist/` - Final executable distribution
- `snake_env/` - Python virtual environment

### Testing
- AI testing automatically tracks moves, scores, and game completion
- Multiple test runs supported for performance analysis
- Built-in loop detection prevents infinite AI cycles

## Game Integration Points

### AI Mode Activation
The main game detects AI mode through:
- Command line `--ai` flag
- Direct `ai_mode=True` parameter to `game_loop()`
- Automatic state sharing via global `game_status` dictionary

### State Synchronization
- Game updates AI state after each frame via `update_snake_state()`
- AI accesses current state through `self.game_state`
- Bi-directional communication ensures AI has real-time game information

### Movement Integration
AI decisions integrate seamlessly with existing keyboard input system:
- AI outputs direction strings ("UP", "DOWN", "LEFT", "RIGHT")
- Directions convert to coordinate changes matching keyboard controls
- Same collision and boundary checking applies to both human and AI players