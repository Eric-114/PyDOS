"""
更新日志
Develop Interview:
    0.1:
        20250322-rc5 : Review & +更新日志
        20250322-rc6 : 更改名称，分开DOS与Main，为GUI准备。
        20250322-rc7 : 着手研发GUI，用Main开启DOS
    0.2:
        20250322-rc8 : GUI 启动！
"""

import tkinter as tk
import json
import os
from tkinter import messagebox
from PyDOS2 import PyDOS_Use

preparation="PyDOS 操作系统\n作者: 白僵菌\n版本: PyDOS Develop Interview 0.1\n欢迎使用！"

if __name__ == "__main__":
    root = tk.Tk()
    app = PyDOS_Use(root)
    file_size = os.path.getsize("files.txt")
    app.display_output(preparation)
    app.display_output(f'\n\n文件大小:{file_size/1000}KB\n')
    root.mainloop()
