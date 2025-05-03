'''
PyDOW Preview 0.01 - 20250501
'''
from tkinter import *
import json
import os
class PyDOW_Use:
    def __init__(self, root):
        #root:主窗口
        self.root = root
        root.title('PyDOW')
        self.current_path = ["C:\\"]

        root.configure(bg=self.word_las('User_Color'))
        self.auto_setup_default_icons()
        self.load_desktop_apps()

        from tkinter import Label
        import time as t

        self.time_label = Label(root, text=self.time_geshi(), bg="lightblue", font=('Courier New', 12))
        self.time_label.grid(row=0, column=0, columnspan=4, sticky='ew', padx=10, pady=5)

        self.root.after(0, self.update_time)

    def time_geshi(self):
        import time as t
        a = t.ctime()
        words = a.split()
        def month(en):
            if en == "Jan":
                return "1月"
            elif en == "Feb":
                return "2月"
            elif en == "Mar":
                return "3月"
            elif en == "Apr":
                return "4月"
            elif en == "May":
                return "5月"
            elif en == "Jun":
                return "6月"
            elif en == "Jul":
                return "7月"
            elif en =="Aug":
                return "8月"
            elif en == "Sep":
                return "9月"
            elif en == "Oct":
                return "10月"
            elif en == "Nov":
                return "11月"
            else:
                return "12月"
        b = month(words[1])+words[2]+"日"+' '+words[3]
        return b
    def update_time(self):
        import time as t
        self.time_label.config(text=self.time_geshi())
        self.root.after(1000, self.update_time)

    # 名字由来：file_[load and save] :)
    def file_las(self, file, mode, data=None):
        filename = file + ".txt"
        from tkinter import messagebox
        if mode == 'load':
            try:
                if os.path.exists(filename):
                    with open(filename, "r", encoding="utf-8") as f:
                        return json.load(f)
                return self.create_default_fs()
            except Exception as e:
                messagebox.showerror("错误", f"无法加载 {file}: {str(e)}")
                return self.create_default_fs()
        elif mode == 'save':
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                messagebox.showerror("错误", f"无法保存 {file}: {str(e)}")
    # 同理，处理一个单词
    def word_las(self, file, new_word=None):
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

    def add_desktop_app(self, app_name, where,row=None, col=None):
        desktop_config = self.file_las(where, "load")
        if desktop_config is None:
            desktop_config = {}
        if row is None or col is None:
            max_per_row = 4
            used_positions = set((int(r), int(c)) for r, c in desktop_config.values())
            idx = len(desktop_config)
            while True:
                row_auto = idx // max_per_row
                col_auto = idx % max_per_row
                if (row_auto, col_auto) not in used_positions:
                    row, col = row_auto, col_auto
                    break
                idx += 1
        else:
            row, col = int(row), int(col)
        desktop_config[app_name] = [row, col]
        self.file_las(where, "save", desktop_config)
        self.create_app_icon(app_name, row, col)

    def create_app_icon(self, app_name, row, col):
        icon = Button(
            self.root,
            text=app_name,
            width=10,
            height=3,
            bg='gray',
            fg='white',
            command=lambda: self.open_app_test(app_name)
        )
        icon.grid(row=row, column=col, padx=10, pady=10)

    def open_app_test(self, app_name):
        match app_name:
            case "此电脑":
                self.open_this_pc_window()
            case "DOS":
                self.open_DOS()
            case '退出':
                self.open_exit()
            case '设置':
                self.open_settings_window()
            case _:
                print(f"打开{app_name}")

    def load_desktop_apps(self):
        desktop_config = self.file_las("desktop_apps_sign_place", "load")
        for app_name, pos in desktop_config.items():
            self.create_app_icon(app_name, int(pos[0]), int(pos[1]))

    def auto_setup_default_icons(self):
        """
        自动初始化默认图标（如果配置文件为空）
        """
        desktop_config = self.file_las("desktop_apps_sign_place", "load")
        if not desktop_config:
            self.add_desktop_app("此电脑",'desktop_apps_sign_place')
            self.add_desktop_app("回收站", 'desktop_apps_sign_place')
            self.add_desktop_app("文档",'desktop_apps_sign_place')
            self.add_desktop_app("设置",'desktop_apps_sign_place')


    #如何使用：
    '''
    添加应用：
        app.add_desktop_app("游戏", row=2)
    
    '''

    #此电脑

    def open_DOS(self):
        from PyDOS2 import PyDOS_Use
        import tkinter as tk
        root = tk.Tk()
        preparation = "PyDOS 操作系统\n作者: 白僵菌\n版本: PyDOS Develop Interview 0.1\n欢迎使用！"
        app = PyDOS_Use(root)
        file_size = os.path.getsize("files.txt")
        app.display_output(preparation)
        app.display_output(f'\n\n文件大小:{file_size / 1000}KB\n')
        root.mainloop()

    def open_exit(self):
        self.root.destroy()

    def open_settings_window(self):
        settings_window = Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("500x400")
        settings_window.configure(bg='black')

        Label(
            settings_window,
            text="系统设置",
            bg='black',
            fg='#00FF00',
            font=('Courier New', 16, 'bold'),
            anchor='w'
        ).pack(pady=10)

        frame = Frame(settings_window, bg='black')
        frame.pack(fill='both', expand=True, padx=20)

        # 添加“关于”按钮
        about_btn = Button(
            frame,
            text="关于",
            width=20,
            height=2,
            bg='gray',
            fg='white',
            command=self.open_about_window
        )
        about_btn.pack(pady=10)

    def open_about_window(self):
        about_window = Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("400x300")
        about_window.configure(bg='black')

        Label(
            about_window,
            text="PyDOW 操作系统",
            bg='black',
            fg='#00FF00',
            font=('Courier New', 16, 'bold')
        ).pack(pady=20)

        a = self.word_las('preparation1')

        info = (
            "版本: PyDOW"+a+"\n"
            "发布日期: 2025-05-01\n"
            "开发者: 白僵菌\n"
        )

        Label(
            about_window,
            text=info,
            bg='black',
            fg='#00FF00',
            font=('Courier New', 12),
            justify=LEFT,
            anchor='w'
        ).pack(padx=20, pady=10)

        close_btn = Button(
            about_window,
            text="关闭",
            width=10,
            height=1,
            bg='gray',
            fg='white',
            command=about_window.destroy
        )
        close_btn.pack(pady=10)

    def open_this_pc_window(self):
        fs = self.file_las("files", "load")
        if not fs or "C:\\" not in fs:
            messagebox.showerror("错误", "文件系统损坏或未找到 C:\\ 目录")
            return
        root_fs = fs["C:\\"]
        bg_color = self.word_las('User_Color') or 'black'
        text_color = '#00FF00'
        pc_window = Toplevel(self.root)
        pc_window.title("此电脑 - C:\\")
        pc_window.geometry("800x600")
        pc_window.configure(bg=bg_color)
        Label(
            pc_window,
            text="此电脑 - C:\\",
            bg=bg_color,
            fg=text_color,
            font=('Courier New', 12, 'bold'),
            anchor='w'
        ).pack(pady=5)
        frame = Frame(pc_window, bg=bg_color)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        max_per_row = 4
        idx = 0

        def create_icon(name, is_dir, row, col):
            btn_text = name + ("夹" if is_dir else "")
            btn = Button(
                frame,
                text=btn_text,
                width=15,
                height=3,
                bg='gray',
                fg='white',
                font=('Courier New', 10),
                anchor='w',
                justify='left'
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

            def on_double_click(e=None):
                path = "\\".join(self.current_path + [name])
                if is_dir:
                    self.open_subfolder_window(path)
                else:
                    self.open_file_content_window(path)

            btn.bind("<Double-Button-1>", on_double_click)

            def on_right_click(e):
                menu = Menu(self.root, tearoff=0)
                menu.add_command(label="新建")
                menu.add_command(label="删除")
                menu.add_command(label="重命名")
                menu.tk_popup(e.x_root, e.y_root)
                menu.tk_unpost()

            btn.bind("<Button-3>", on_right_click)  # 右键点击

        for name, content in root_fs.items():
            row = idx // max_per_row
            col = idx % max_per_row
            is_dir = isinstance(content, dict)
            create_icon(name, is_dir, row, col)
            idx += 1

    def open_subfolder_window(self, folder_path):
        fs = self.file_las("files", "load")
        if folder_path.startswith("C:\\"):
            current = fs.get("C:\\", {})
            parts = folder_path[len("C:\\"):].strip("\\").split("\\")
        else:
            parts = [p for p in folder_path.split("\\") if p]
            current = fs
        for part in parts:
            current = current.get(part, {})
            if not isinstance(current, dict):
                messagebox.showerror("错误", f"路径无效: {folder_path}")
                return
        sub_window = Toplevel(self.root)
        sub_window.title(folder_path)
        sub_window.geometry("800x600")
        sub_window.configure(bg='black')
        Label(
            sub_window,
            text=folder_path,
            bg='black',
            fg='#00FF00',
            font=('Courier New', 12, 'bold'),
            anchor='w'
        ).pack(pady=5)
        frame = Frame(sub_window, bg='black')
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        max_per_row = 4
        idx = 0
        for name, content in current.items():
            row = idx // max_per_row
            col = idx % max_per_row
            is_dir = isinstance(content, dict)
            self.create_icon_in_frame(frame, name, is_dir, row, col, folder_path)
            idx += 1

    def create_icon_in_frame(self, frame, name, is_dir, row, col, parent_path):
        btn_text = name + ("夹" if is_dir else "")
        btn = Button(
            frame,
            text=btn_text,
            width=15,
            height=3,
            bg='gray',
            fg='white',
            font=('Courier New', 10),
            anchor='w',
            justify='left'
        )
        btn.grid(row=row, column=col, padx=5, pady=5)

        def on_double_click(e=None):
            full_path = f"{parent_path}\\{name}"
            if is_dir:
                self.open_subfolder_window(full_path)
            else:
                self.open_file_content_window(full_path)

        btn.bind("<Double-Button-1>", on_double_click)

    def open_file_content_window(self, file_path):
        fs = self.file_las("files", "load")

        # 解析路径
        if file_path.startswith("C:\\"):
            current = fs.get("C:\\", {})
            parts = file_path[len("C:\\"):].strip("\\").split("\\")
        else:
            parts = [p for p in file_path.split("\\") if p]
            current = fs

        for part in parts[:-1]:
            current = current.get(part, {})
            if not isinstance(current, dict):
                messagebox.showerror("错误", f"找不到文件: {file_path}")
                return

        filename = parts[-1]
        content = current.get(filename, "")

        if not isinstance(content, str):
            messagebox.showerror("错误", f"无法打开非文本文件: {filename}")
            return

        # 创建编辑窗口
        edit_window = Toplevel(self.root)
        edit_window.title(f"编辑 - {filename}")
        edit_window.geometry("600x400")


        toolbar = Frame(edit_window)
        toolbar.pack(side=TOP, fill=X, padx=5, pady=5)


        def save_file():
            new_content = text_area.get("1.0", END).strip()
            current[filename] = new_content
            self.file_las("files", "save", fs)
            from tkinter import messagebox
            messagebox.showinfo("提示", "保存成功！")
            edit_window.destroy()

        # 保存按钮
        save_btn = Button(
            toolbar,
            text="保存",
            width=10,
            height=2,
            bg='green',
            fg='white',
            command=save_file
        )
        save_btn.pack(side=LEFT, padx=2, pady=2)

        cancel_btn = Button(
            toolbar,
            text="取消",
            width=10,
            height=2,
            bg='gray',
            fg='white',
            command=edit_window.destroy
        )
        cancel_btn.pack(side=LEFT, padx=2, pady=2)

        exit_btn = Button(
            toolbar,
            text="退出",
            width=10,
            height=2,
            bg='gray',
            fg='white',
            command=edit_window.destroy
        )
        exit_btn.pack(side=LEFT, padx=2, pady=2)

        # 文本区域
        text_area = Text(edit_window, wrap='word', bg='black', fg='white', font=('Courier New', 10))
        text_area.pack(fill='both', expand=True, padx=5, pady=0)
        text_area.insert('1.0', content)