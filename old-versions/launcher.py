import customtkinter as CTk
import minecraft_launcher_lib
import subprocess
from uuid import uuid1
from PIL import Image
import time

#консоль приветствие
print("Привет это консоль!")


def __init__(self):
    super().__init__()

class ToplevelWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.geometry("400x300")
        self.title("settings")

        self.label = CTk.CTkLabel(self, text="Settings")
        self.label.pack(padx=20, pady=20)

#Создание окна
class App(CTk.CTk):
    def __init__(self):
        super().__init__()
        #создание переменных ника и версии
        self.player_nickname = ""
        self.past_versionid = ""

        #выбор дирректории
            #directory = filedialog.askdirectory()
            #print(directory)



        #Получение ника
        def past_nickname(self):
            self.player_nickname = "{}".format(self.nickname_entry.get())
            #Если ник не введен присвоить значение стив
            if self.player_nickname == '':
                self.player_nickname = 'Steave'
            #вывод ника в консоль
            print("Ник игрока: ", self.player_nickname)

        #Получение версии
        def past_version(self):
            self.past_versionid = "{}".format(self.version_menu.get())
            #вывод версии в консоль
            print(print("Выбраная версия: "),self.past_versionid)

        #создание списка версий
        versionsId = []

        def update_progress(self, progress, max_progress):
            print()


        #запуск игры
        def start_game():
            past_nickname(self)
            past_version(self)

            minecraft_launcher_lib.install.install_minecraft_version(versionid=self.past_versionid, minecraft_directory=".minecraft")

            opions = {
                'username': self.player_nickname,
                'uuid': str(uuid1()),
                'token': ''
            }

            subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=self.past_versionid, minecraft_directory=".minecraft", options=opions))

        #размер окна и настройка
        self.geometry("1024x570")
            #название лаунчера
        self.title("FreshLauncher")
            #запрет на изменение размера окна по X и Y
        self.resizable(False, False)
            #иконка лаунчера
        self.after(201, lambda :self.iconbitmap('icon.ico'))

        self.grid_columnconfigure(0, weight=1)

        #лого посреди окна
        self.logo = CTk.CTkImage(dark_image=Image.open("../images/LauncherTitle.png"), size=(480, 120))
        self.logo_lavel = CTk.CTkLabel(master=self, text="", image=self.logo)
        self.logo_lavel.grid(row=0, column=0, pady=(30, 0))

        #создание фрейма
        self.ui_frame = CTk.CTkFrame(self, corner_radius=15, width=380, height=300)
        self.ui_frame.grid(row=1, column=0, padx=(324, 0), pady=(155, 0), sticky="nsw")

        #поле ввода ника
        self.nickname_entry = CTk.CTkEntry(master=self.ui_frame, corner_radius=13, width=300, height=50, placeholder_text="nickname")
        self.nickname_entry.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="w")

        #занисение версий в список versionId
        for version in minecraft_launcher_lib.utils.get_version_list():
            if version['type'] == "release":
                versionsId.append(version['id'])
        print(versionsId)

        #меню выбора версий
        self.version_menu = CTk.CTkComboBox(self.ui_frame, corner_radius=13, width=300, height=50, values=versionsId)
        self.version_menu.grid(row=2, column=0, padx=(20, 20), pady=(10, 20))

        #кнопка играть
        self.play_button = CTk.CTkButton(master=self.ui_frame, width=300, height=50, corner_radius=13, border_width=0, text="Играть", command=start_game)
        self.play_button.grid(row=3, column=0, padx=(20, 20), pady=(10, 20), sticky="w")

        self.toplevel_window = None

        #Прогресс бар
        self.Progress_Bar = CTk.CTkProgressBar(self.ui_frame)
        self.Progress_Bar.grid()
        self.Progress_Bar.set(0)




    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


if __name__ == "__main__":
    app = App()
    app.mainloop()