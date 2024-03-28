# 在 bing_searchs_app.py 中
import tkinter as tk
from tkinter import messagebox
import pyautogui
import random
import time
import threading
import pyperclip
import pygetwindow as gw
from utils.wordlist import word_list
from utils.consent_window import ConsentWindow


class BingSearchsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JustNoBingSearch v1.2")
        self.root.geometry("600x350")
        self.root.minsize(600, 350)
        self.root.maxsize(600, 350)
        self.root.withdraw()

        self.consent_given = False
        self.auto_open_edge = tk.BooleanVar(value=False)

        self.consent_window = ConsentWindow(
            tk.Toplevel(), self.on_consent_given)

    def show_about_info(self):
        about_info = "作者: 苍策\n版本: v1.2\n\n一个用于执行必应搜索的简单程序。"
        messagebox.showinfo("关于", about_info)

    def on_consent_given(self, consent):
        if consent:
            self.consent_given = True
            self.initialize_ui()
            self.root.deiconify()
        else:
            self.root.destroy()

    def get_edge_window_handle(self):
        edge_window = None
        for window in gw.getAllWindows():
            if "Edge" in window.title:
                edge_window = window
                break

        if edge_window is None and self.auto_open_edge.get():
            pyautogui.hotkey('ctrl', 'esc')  # 打开开始菜单
            time.sleep(1)
            pyautogui.write('Edge')
            time.sleep(1)
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(5)  # 等待Edge浏览器打开
            edge_window = gw.getWindowsWithTitle("Edge")[0]

        return edge_window

    def get_target_window(self):
        if not self.consent_given:
            return

        self.prompt_label.config(text="程序正在自动搜寻目标窗口：Edge")
        self.root.update()
        time.sleep(4)
        self.target_window = self.get_edge_window_handle()
        if self.target_window is not None:
            window_title = self.target_window.title
            self.target_text.config(state=tk.NORMAL)
            self.target_text.delete('1.0', tk.END)
            self.target_text.insert(tk.END, f"目标窗口: {window_title}\n")
            self.target_text.config(state=tk.DISABLED)
            self.start_action()
        else:
            self.target_text.config(state=tk.NORMAL)
            self.target_text.delete('1.0', tk.END)
            self.target_text.insert(tk.END, "未找到目标窗口，请手动聚焦到目标窗口\n")
            self.target_text.config(state=tk.DISABLED)
        self.prompt_label.config(text="")

    def initialize_ui(self):
        self.label = tk.Label(self.root, text="执行次数:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.auto_open_edge_checkbox = tk.Checkbutton(
            self.root, text="若Edge窗口不存在，自动打开Edge", variable=self.auto_open_edge)
        self.auto_open_edge_checkbox.pack()

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()

        self.get_window_button = tk.Button(
            self.buttons_frame, text="获取目标窗口并开始", command=self.get_target_window)
        self.get_window_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            self.buttons_frame, text="暂停", command=self.pause_task, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            self.buttons_frame, text="停止", command=self.stop_task, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.target_text = tk.Text(self.root, height=4, width=50)
        self.target_text.pack()
        self.target_text.tag_configure("center", justify='center')
        self.target_text.config(state=tk.DISABLED)

        self.remaining_text = tk.Text(self.root, height=4, width=50)
        self.remaining_text.pack()
        self.remaining_text.tag_configure("center", justify='center')
        self.remaining_text.config(state=tk.DISABLED)

        self.prompt_label = tk.Label(self.root, text="")
        self.prompt_label.pack()

        self.click_position = (720, 120)
        self.target_window = None
        self.running = False
        self.pause = False

        # 创建菜单栏
        menubar = tk.Menu(self.root)

        # 创建下拉菜单
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="关于", command=self.show_about_info)

        # 将下拉菜单添加到菜单栏
        menubar.add_cascade(label="帮助", menu=about_menu)

        # 将菜单栏添加到主窗口
        self.root.config(menu=menubar)

        # 确保主功能窗口被置顶
        self.root.attributes('-topmost', True)

    def pause_task(self):
        if self.running:
            self.pause = not self.pause
            if self.pause:
                self.pause_button.config(text="继续")
            else:
                self.pause_button.config(text="暂停")

    def stop_task(self):
        self.running = False
        self.pause = False
        self.pause_button.config(text="暂停", state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def run_task(self, n):
        if self.target_window is None:
            self.target_text.config(state=tk.NORMAL)
            self.target_text.delete('1.0', tk.END)
            self.target_text.insert(tk.END, "未找到目标窗口，请手动聚焦到目标窗口\n")
            self.target_text.config(state=tk.DISABLED)
            return

        remaining_times = n
        time.sleep(5)
        self.running = True
        self.pause = False
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        for i in range(n):
            if not self.running:
                break
            if self.pause:
                continue
            try:
                self.target_window.activate()
                pyautogui.hotkey('ctrl', 'e')
                time.sleep(2)
                word = random.choice(word_list)
                # 使用pyperclip直接将单词粘贴到搜索框
                pyperclip.copy(word)
                pyautogui.hotkey('ctrl', 'v')  # 粘贴
                pyautogui.press('enter')
                time.sleep(4)

                remaining_times -= 1
                self.remaining_text.config(state=tk.NORMAL)
                self.remaining_text.delete('1.0', tk.END)
                self.remaining_text.insert(
                    tk.END, f"剩余次数: {remaining_times}\n")
                self.remaining_text.config(state=tk.DISABLED)
            except Exception as e:
                print("Error:", e)

        self.running = False
        self.pause = False
        self.pause_button.config(text="暂停", state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.remaining_text.config(state=tk.NORMAL)
        self.remaining_text.delete('1.0', tk.END)
        self.remaining_text.insert(tk.END, "任务完成！\n")
        self.remaining_text.config(state=tk.DISABLED)

    def start_action(self):
        try:
            n = int(self.entry.get())
            threading.Thread(target=self.run_task,
                             args=(n,), daemon=True).start()
        except ValueError:
            self.remaining_text.config(state=tk.NORMAL)
            self.remaining_text.delete('1.0', tk.END)
            self.remaining_text.insert(tk.END, "请输入有效的次数\n")
            self.remaining_text.config(state=tk.DISABLED)
