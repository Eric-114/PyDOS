"""
更新日志
Develop Interview:
    0.1:
        20250322-rc5 : Review & +更新日志
        20250322-rc6 : 更改名称，分开DOS与Main，为GUI准备。
        20250322-rc7 : 着手研发GUI，用Main开启DOS
    0.2:
        0.21:
            20250322-rc1 : GUI 启动！
            20250502-rc2 : PyDOW初具规模
            20250502-rc3 : 设置
"""

import tkinter as tk
import json
import os
from tkinter import messagebox
from PyDOS2 import PyDOS_Use
from PyDOW import PyDOW_Use


def word_las(file, new_word=None):
    filename = file + ".txt"
    from tkinter import messagebox

    try:
        # 如果是写入模式
        if new_word is not None:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_word.strip())
            return True

        # 如果是读取模式
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return content
        return None

    except Exception as e:
        messagebox.showerror("错误", f"文件操作失败: {str(e)}")
        return None

a=word_las('preparation1')

preparation="PyDOS 操作系统\n作者: 白僵菌\n版本: PyDOS"+a+"\n欢迎使用！"

if __name__ == "__main__":
    root = tk.Tk()
    app = PyDOS_Use(root)
    file_size = os.path.getsize("files.txt")
    app.display_output(preparation)
    app.display_output(f'\n\n文件大小:{file_size/1000}KB\n')
    root.mainloop()
