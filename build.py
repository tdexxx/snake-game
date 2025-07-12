"""
打包脚本 - 将贪吃蛇游戏打包为exe文件
"""
import os
import sys
import shutil

def main():
    print("开始打包贪吃蛇游戏...")
    
    # 确保 PyInstaller 已安装并降级到稳定版本
    os.system("pip install pyinstaller==5.13.2")
    
    # 创建打包命令
    cmd = ('pyinstaller '
           '--name "贪吃蛇" '  # 指定输出文件名
           '--add-data "simhei.ttf;." '  # 添加字体文件
           '--clean '          # 清理临时文件
           '--noconfirm '      # 不确认覆盖
           '--specpath build ' # 指定spec文件位置
           '"贪吃蛇.py"')      # 主程序文件
    
    # 执行打包命令
    print("正在打包...")
    os.system(cmd)
    
    # 复制额外文件到dist目录
    dist_path = os.path.join("dist", "贪吃蛇")
    if not os.path.exists(dist_path):
        print(f"创建目录: {dist_path}")
        os.makedirs(dist_path)
    
    # 复制主程序和AI测试相关文件
    exe_file = os.path.join("dist", "贪吃蛇.exe")
    if os.path.exists(exe_file):
        shutil.move(exe_file, os.path.join(dist_path, "贪吃蛇.exe"))
        shutil.copy2("snake_test.py", dist_path)
        shutil.copy2("run_ai_test.py", dist_path)
        shutil.copy2("simhei.ttf", dist_path)
        print("已复制所有必要文件到打包目录")
    else:
        print("错误：未找到生成的exe文件")
    
    print("\n打包完成！")
    print(f"可执行文件位于: {dist_path}")
    print("目录中包含:")
    print("- 贪吃蛇.exe (主游戏程序)")
    print("- snake_test.py (AI测试系统)")
    print("- run_ai_test.py (AI测试运行器)")
    print("- simhei.ttf (字体文件)")

if __name__ == "__main__":
    main()
