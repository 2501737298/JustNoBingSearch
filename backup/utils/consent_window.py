import tkinter as tk


class ConsentWindow:
    def __init__(self, master, callback):
        self.master = master
        master.title("说明")
        master.geometry("300x150")
        master.resizable(False, False)
        master.attributes('-topmost', True)

        self.label = tk.Label(master, text="本程序可能在您的剪贴板内写入词典数据，\n继续使用视为同意")
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.yes_button = tk.Button(
            self.button_frame, text="同意", command=self.on_yes)
        self.yes_button.pack(side=tk.LEFT, padx=10)

        self.no_button = tk.Button(
            self.button_frame, text="拒绝", command=self.on_no)
        self.no_button.pack(side=tk.LEFT, padx=10)

        self.callback = callback

        master.protocol("WM_DELETE_WINDOW", self.on_no)

    def on_yes(self):
        self.master.destroy()
        self.callback(True)

    def on_no(self):
        self.master.destroy()
        self.callback(False)
