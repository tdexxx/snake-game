"""
贪吃蛇AI测试脚本
使用方法:
python run_ai_test.py [次数]
"""

import sys
import time
from 贪吃蛇 import game_loop

def run_single_test():
    """运行单次AI测试"""
    print("开始AI测试...")
    start_time = time.time()
    game_loop(ai_mode=True)
    end_time = time.time()
    print(f"测试完成! 耗时: {end_time - start_time:.2f}秒")

def main():
    """运行AI测试"""
    # 获取测试次数
    test_count = 1
    if len(sys.argv) > 1:
        try:
            test_count = int(sys.argv[1])
        except ValueError:
            print("参数错误：请提供有效的测试次数")
            return

    # 运行指定次数的测试
    print(f"将进行 {test_count} 次AI测试")
    for i in range(test_count):
        print(f"\n开始第 {i+1} 次测试...")
        run_single_test()

if __name__ == "__main__":
    main()
