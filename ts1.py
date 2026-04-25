from typing import Sized

from customtkinter import *

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.frame = CTkFrame(self, width=200, height=self.winfo_height())
        self.frame.configure(width=0)
        self.frame.pack_propagate(False)
        self.title("Max")
        self.frame.place(x=0, y=0)
        self.show_menu = False
        self.frame_width = 0

        self.label = CTkLabel(self.frame, text="your name")
        self.label.pack(pady=30)

        self.entry = CTkEntry(self.frame)
        self.entry.pack()

        self.btn = CTkButton(self, text=">")
        self.btn.place(x=0, y=0)

        self.theme = CTkOptionMenu(self.frame,values=["dark","light"], command=change_theme)
        self.theme.pack(side="bottom",pady=20)

        self.menu_show_speed = 20

        self.chat_text = CTkTextbox(self,state="disabled")
        self.chat_text.place(x=0,y=30)


        self.message_input = CTkEntry(self, placeholder_text="print")
        self.message_input.place(x=0,y=250)

        self.send_btn = CTkButton(self, text="send",width=40, height=40)
        self.send_btn.place(x=200,y=250)

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.close_menu()
        else:
            self.is_show_menu = True
            self.show_menu()

    def show_menu(self):
        if self.frame_width <= 200:
            self.frame_width += self.menu_show_speed
            self.frame.configure(width=self.frame_width, text='<')
            if self.frame_width >= 400:
                self.btn.configure(width=self.frame_width, text='<')
        if self.is_show_menu:
            self.after(20, self.show_menu )


    def close_menu(self):
        if self.frame_width >= 0:
            self.frame_width -= self.menu_show_speed
            self.frame.configure(width=self.frame_width)
            if self.frame_width >= 30:
                self.btn.configure(width=self.frame_width, text='>')
        if not self.is_show_menu:
            self.after(20, self.close_menu)

    def change_theme(self, value):
        if value == "dark":
            set_appearance_mode('dark')
        else:
            set_appearance_mode('light')

    def adaptive_ui(self):
        self.chat_text.configure(width=self.winfo_width() - self.frame.winfo_width(), height=self.winfo_height()  - self.message_input.winfo_height() - 30)
        self.chat_text.place(x=self.frame.winfo_width() - 1)

        self.massage_input.configure(width=self.winfo_width() - self.frame.winfo_width() - self.send_buttom.winfo_width())
        self.massage_input.place(x=self.frame.winfo_width(), y=self.winfo_height() - self.send_buttom.winfo_width())

        self.send_buttom.place(x=self.winfo_width() - self.send_buttom.winfo_width(), y=self.winfo_height() - self.send_buttom.winfo_height())

        self.after(20, self.adaptive_ui)

    def add_message(self, text):
        self.chat_text.configure(state="normal")
        self.chat_text.insert(END, 'Я: ' +  text + '\n')
        self.chat_text.configure(state="disabled")

    def send_message(self):
        massage = self.massage_input.get()

        if massage:
            self.username =  self.entry.get()
            self.add_message(f"{self.Username}: {massage}")
            data = f"TEXT@{self.username}@{massage}\n"
            try:
                self.sock.sendall(data.encode('utf-8'))
            except:
                pass
        self.massege_input.delete(0,END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096).decode('utf-8')
                if not chunk: break
                buffer += chunk
                while '\n' in buffer:
                    line, buffer  = buffer.split('\n',1)
                    parts = line.split('@',2)
                    if len(parts) >= 2 and parts[1] != self.username:
                        self.add_message(f"{parts[1]}: {parts[2]}")
            except:
                break


win = MainWindow()
win.mainloop()