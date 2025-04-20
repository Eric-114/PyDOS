

'''
类
SAVE_FILE   - 文件系统存储文件名

create_default_fs --> 备用，防止没有 files.txt
state='disabled'  --> 禁止编辑
padx=5 & pady=5   --> 内边距
args              --> 剩余部分内容，如Users\路姐.docx 
'''

preparation="PyDOS 操作系统\n作者: 白僵菌\n版本: PyDOS Develop Interview 0.1\n欢迎使用！\n欢迎在B站关注【白大僵菌】！"

import tkinter as tk
import json
import os
from tkinter import messagebox
import pygame,sys
import random
from pygame.locals import *


class PyDOS_Use:
    def __init__(self, master):
        self.master = master
        master.title(preparation)
        master.configure(bg='black')

        # 加载文件
        self.filesystem = self.load_filesystem()
        self.current_path = ["C:\\"]
        self.create_widgets()
        self.update_prompt()

    #Forever
    def load_filesystem(self):
        try:
            if os.path.exists("files.txt"):
                with open("files.txt", "r", encoding="utf-8") as f:
                    return json.load(f)
            return self.create_default_fs()
        except Exception as e:
            messagebox.showerror("错误", f"无法加载: {str(e)}")
            return self.create_default_fs()

    def save_filesystem(self):
        with open("files.txt", "w", encoding="utf-8") as f:
            json.dump(self.filesystem, f, indent=2, ensure_ascii=False)

    def create_default_fs(self):
        return {
            "C:\\": {
                "readme.txt": "暂未发现 files.txt ，为正常运行，已进入访客模式",
                "USERS": {
                    "Desktop": {},
                    "Documents": {}
                }
            }
        }

    #GUI
    def create_widgets(self):
        # 输出窗口
        self.output_text = tk.Text(
            self.master, height=25, width=80, bg='black', fg='#00FF00',
            font=('Courier New', 10), state='disabled'
        )
        self.output_text.pack(padx=5, pady=5)

        # 输入框
        self.input_entry = tk.Entry(
            self.master, width=80, bg='black', fg='#00FF00',
            font=('Courier New', 10)
        )
        self.input_entry.pack(padx=5, pady=5)
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus_set() # 设置焦点

    def update_prompt(self):
        self.prompt = "\\".join(self.current_path) + "> "
        self.input_entry.delete(0, tk.END)        # 清空输入框
        self.input_entry.insert(0, self.prompt)  # 插入新的提示符
        self.input_entry.icursor(tk.END)               # 将光标移动到末尾

    #SYSTEM
    def process_command(self, event):
        full_command = self.input_entry.get().replace(self.prompt, "").strip()
        if not full_command:
            self.display_output("Wow! 头抬起！记得开启功率。(Doge)")
            return

        # 显示命令
        self.display_output(f"\n{self.prompt}{full_command}")

        # 执行命令
        self.execute_command(full_command)

        # 更新提示符
        self.update_prompt()

    def display_output(self, text):
        self.output_text.configure(state='normal')  # 启用输出窗口编辑
        self.output_text.insert(tk.END, text)  # 插入文本
        self.output_text.see(tk.END)  # 滚动到底部
        self.output_text.configure(state='disabled')  # 禁用输出窗口编辑

    def execute_command(self, command):
        command_map = {
            'help': self.cmd_help,
            'cls': self.cmd_cls,
            'exit': self.cmd_exit,
            'ver': self.cmd_ver,
            'dir': self.cmd_dir,
            'type': self.cmd_type,
            'cd': self.cmd_cd,
            'edit': self.cmd_edit,
            'mkdir': self.cmd_mkdir,
            'del': self.cmd_del,
            'copy': self.cmd_copy,
            'game' : self.cmd_game
        }
        parts = command.split()
        if not parts:
            return
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in command_map:
            try:
                command_map[cmd](args)
            except Exception as e:
                self.display_output(f"\n错误: {str(e)}")
        else:
            self.display_output(f"\n'{cmd}' 不是有效命令")

    def cmd_help(self, args):
        help_text = """
        支持命令:
        HELP    显示帮助信息
        CLS     清屏
        DIR     列出目录内容
        CD      切换目录
        TYPE    显示文件内容
        EDIT    编辑文件
        COPY    复制文件
        DEL     删除文件
        MKDIR   创建目录
        EXIT    退出系统
        ???     隐藏彩蛋 :)
        GAME    游戏 （开发中）
        """
        self.display_output(help_text)

    def cmd_cls(self, args):
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state='disabled')

    def cmd_exit(self, args):
        self.master.destroy()

    def cmd_ver(self, args):
        self.display_output("\n"+preparation)

    def get_current_dir(self):
        current = self.filesystem
        for part in self.current_path:
            current = current.get(part, {})
        return current

    def cmd_dir(self, args):
        current_dir = self.get_current_dir()
        output = "\n"
        for name, content in current_dir.items():
            output += f"{'<DIR>' if isinstance(content, dict) else 'FILE':12} {name}\n"
        self.display_output(output)
    
    def cmd_game(self,args):
        from test import Use
        a=Use()
        a.Use2()

    def cmd_type(self, args):
        if not args:
            self.display_output("\n用法: TYPE 文件名")
            return

        filename = args[0]
        current_dir = self.get_current_dir()
        if filename in current_dir and isinstance(current_dir[filename], str):
            self.display_output(f"\n{current_dir[filename]}")
        else:
            self.display_output(f"\n文件未找到: {filename}")

    def cmd_cd(self, args):
        if not args:
            self.display_output(f"\n当前目录: {'//'.join(self.current_path)}")
            return

        target = args[0]
        if target == ".." or target == "back":
            if len(self.current_path) > 1:
                self.current_path.pop()    #返回上一级
        else:
            current_dir = self.get_current_dir()
            if target in current_dir and isinstance(current_dir[target], dict):
                self.current_path.append(target)
            else:
                self.display_output(f"\n路径无效: {target}")

    def cmd_edit(self, args):
        if not args:
            self.display_output("\n用法: EDIT 文件名")
            return

        filename = args[0]
        current_dir = self.get_current_dir()
        content = current_dir.get(filename, "") if isinstance(current_dir.get(filename, ""), str) else ""

        top = tk.Toplevel()
        top.title(f"编辑 {filename}")

        text_editor = tk.Text(top, wrap=tk.WORD, width=60, height=20)
        text_editor.pack(padx=5, pady=5)
        text_editor.insert(tk.END, content)

        def save_file():
            current_dir[filename] = text_editor.get("1.0", tk.END).strip()
            self.save_filesystem()
            self.display_output(f"\n保存成功: {filename}")
            top.destroy()

        tk.Button(top, text="保存", command=save_file).pack(pady=5)

    def cmd_mkdir(self, args):
        if not args:
            self.display_output("\n用法: MKDIR 目录名")
            return

        dirname = args[0]
        current_dir = self.get_current_dir()
        if dirname in current_dir:
            self.display_output(f"\n目录已存在: {dirname}")
        else:
            current_dir[dirname] = {}
            self.save_filesystem()
            self.display_output(f"\n已创建目录: {dirname}")

    def cmd_del(self, args):
        if not args:
            self.display_output("\n用法: DEL 文件名")
            return

        filename = args[0]
        current_dir = self.get_current_dir()
        if filename in current_dir and not isinstance(current_dir[filename], dict):
            del current_dir[filename]
            self.save_filesystem()
            self.display_output(f"\n已删除文件: {filename}")
        else:
            self.display_output(f"\n文件未找到: {filename}")
    def cmd_copy(self, args):
        if len(args) != 2:
            self.display_output("\n用法: COPY 源文件 目标路径")
            return

        src, dest = args
        src_dir = self.get_current_dir()
        dest_dir = self.navigate_to_path(dest)

        if not dest_dir or not src_dir.get(src):
            self.display_output(f"\n无效路径或文件不存在")
            return

        dest_dir[os.path.basename(src)] = src_dir[src]
        self.save_filesystem()
        self.display_output(f"\n已复制 {src} 到 {dest}")

    def navigate_to_path(self, path):
        try:
            if path.startswith("C:\\"):
                parts = [p for p in path.split("\\") if p]
                current = self.filesystem
                for part in parts:
                    if part in current and isinstance(current[part], dict):
                        current = current[part]
                    else:
                        return None
                return current
            else:
                current = self.get_current_dir()
                parts = path.split("\\")
                for part in parts:
                    if part in current and isinstance(current[part], dict):
                        current = current[part]
                    else:
                        return None
                return current
        except:
            return None