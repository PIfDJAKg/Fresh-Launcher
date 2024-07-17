import customtkinter as CTk
import minecraft_launcher_lib
import subprocess
import threading
from uuid import uuid1
from PIL import Image, ImageTk
from tkinter import filedialog
import pyglet
import configparser
import pymem
import webbrowser
from CTkScrollableDropdown import *

#создание файла с сохранениями данных
config = configparser.ConfigParser()

#консоль приветствие
print("Привет это консоль!")

def __init__(self):
    super().__init__()

class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        CTk.set_default_color_theme("green")

        #шрифт
        pyglet.font.add_file('JetBrainsMono-Medium.ttf')

        config.read('saved_variables.ini')
        #создание\получение переменных ника и версии
        self.player_nickname = config.get('Nickname', 'player_nick')
        self.past_versionid = ""

        #cохранение\получения файла заднего фона

        #сохранение\получение директории в файл
        self.mc_directory = ".minecraft"

        # получение
        self.mc_directory = config.get('Directory', 'dir')
        # Сохранение
        config['Directory'] = {'dir': self.mc_directory}

        #сохранение\получение количевства выделенной оперативки в файл
        self.memory_mb = 3072
        #получение
        self.memory_mb = int(config.get('Ram_memory', 'ram'))
        #Сохранение
        config['Ram_memory'] = {'ram': self.memory_mb}
        print("RAM: ", self.memory_mb, "mb")

        add_settings_image = ImageTk.PhotoImage(Image.open("../images/settings_icon.png").resize((37, 37)))
        add_info_image = ImageTk.PhotoImage(Image.open("../images/info_icon.png").resize((37, 37)))

        #Получение ника
        def past_nickname(self):
            self.player_nickname = "{}".format(self.nickname_entry.get())
            #Если ник не введен присвоить значение стив
            if self.player_nickname == '':
                self.player_nickname = config.get('Nickname', 'player_nick')
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

        #запуск игры
        def start_game():
            global loader_version
            self.play_button.configure(state="disabled")

            self.progress_bar = CTk.CTkProgressBar(master=self.ui_frame, mode="indeterminnate")
            self.progress_bar.grid()
            self.progress_bar.start()

            past_nickname(self)
            past_version(self)

            #сохранение никнейма в файл
            config['Nickname'] = {'player_nick': self.player_nickname}
            #Запись всех сохранений в файл при нажатии играть
            with open('../saved_variables.ini', 'w') as configfile:
                config.write(configfile)

            opions = {
                'username': self.player_nickname,
                'uuid': str(uuid1()),
                'token': '',
                'jvmArguments': [f'-Xmx{self.memory_mb}M', f'-Xms{self.memory_mb // 2}M']
            }

            if 'fabric' in self.past_versionid:
                fabric_version = self.past_versionid.replace(' fabric','')
                print(fabric_version)
                minecraft_launcher_lib.fabric.install_fabric(fabric_version, self.mc_directory, '0.16.0')
                installed_versions = []
                for mc_versions in minecraft_launcher_lib.utils.get_installed_versions(self.mc_directory):
                    installed_versions.append(mc_versions['id'])
                    loader_version = 'fabric-loader-0.16.0-' + fabric_version
                if loader_version in installed_versions:
                    subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=loader_version, minecraft_directory=self.mc_directory, options=opions))
            else:
                minecraft_launcher_lib.install.install_minecraft_version(versionid=self.past_versionid, minecraft_directory=self.mc_directory)
                subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=self.past_versionid, minecraft_directory=self.mc_directory, options=opions))

            print("RAM: ",self.memory_mb,"mb")

            try:
                pymem.Pymem("Minecraft.exe")
            except:
                print("Игра не запущена")
                self.play_button.configure(state="enable")
                self.progress_bar.destroy()

        game_thread = threading.Thread(target=start_game)
        def start_game_thread():
            self.stop = False
            game_thread.start()



        # получение и расположение программы по центру экрана
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 3
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 3
        self.wm_geometry("+%d+%d" % (x, y))
        self.wm_geometry()

        #размер окна и настройка
        self.geometry("724x407")
            #название лаунчера
        self.title("Fresh Launcher")
            #запрет на изменение размера окна по X и Y
        self.resizable(False, False)
            #иконка лаунчера
        self.after(201, lambda :self.iconbitmap("images/icon.ico"))

        self.grid_columnconfigure(0, weight=1)



        #лого посреди окна
        self.logo = CTk.CTkImage(dark_image=Image.open("../images/background_image.png"), size=(730, 380))
        self.logo_lavel = CTk.CTkLabel(master=self, text="", image=self.logo)
        self.logo_lavel.grid(row=0, column=0, padx=(0, 0), pady=(0, 33))

        #создание фрейма
        self.ui_frame = CTk.CTkFrame(self, corner_radius=0, width=724, height=300)
        self.ui_frame.grid(row=0, column=0, padx=(0, 0), pady=(335, 0), sticky="nsw")

        #создание фрейма доп кнопок
        self.Buttons_frame = CTk.CTkFrame(self, corner_radius=0, width=20, height=100)
        self.Buttons_frame.grid(row=0, column=0, padx=(0, 0), pady=(207, 80), sticky="nsw")

        #поле ввода ника
        self.nickname_entry = CTk.CTkEntry(master=self.ui_frame, corner_radius=13, width=220, height=50, font=("JetBrains Mono Medium", 20), placeholder_text=self.player_nickname)
        self.nickname_entry.grid(row=1, column=0, padx=(12, 10), pady=(10, 20), sticky="w")


        # занисение версий в список versionId
        for version in minecraft_launcher_lib.utils.get_version_list():
            if version['type'] == "release":
                versionsId.append(version['id'])
                if minecraft_launcher_lib.fabric.is_minecraft_version_supported(version['id']):
                    versionsId.append(version['id'] + ' fabric')


        #меню выбора версий
        self.version_menu = CTk.CTkOptionMenu(self.ui_frame, corner_radius=13, fg_color='#088f00', button_color='#087501', button_hover_color='#066900',font=("JetBrains Mono Medium", 20), width=220, height=50, values=versionsId)
        self.version_menu.grid(row=1, column=1, padx=(10, 10), pady=(10, 20))

        #красивый скролл бар для меню выбора версий
        CTkScrollableDropdown(self.version_menu, values=versionsId, hover_color='#087301')

        #кнопка играть
        self.play_button = CTk.CTkButton(master=self.ui_frame, fg_color='#088f00', hover_color='#087301', width=220, height=50, corner_radius=13, border_width=0, text="Играть",font=("JetBrains Mono Medium", 25), command=lambda: start_game_thread())
        self.play_button.grid(row=1, column=2, padx=(10, 13), pady=(10, 20), sticky="w")




        #кнопка настроек
        self.settings_button = CTk.CTkButton(master=self.Buttons_frame, width=30, height=45, fg_color='#088f00', hover_color='#087301', corner_radius=13, border_width=0, image=add_settings_image, text="", command=lambda: settings_win())
        self.settings_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 70), sticky="w")

        #кнопка информации(открытие офф тг)
        self.directory_button = CTk.CTkButton(master=self.Buttons_frame, width=30, height=45, fg_color='#088f00', hover_color='#087301', corner_radius=13, border_width=0, image=add_info_image, text="", command=lambda: webbrowser.open_new_tab('t.me/pidjak_hub'))
        self.directory_button.grid(row=3, column=0, padx=(10, 10), pady=(60, 10), sticky="w")

        #текст версии
        #self.launch_version_label = CTk.CTkLabel(master=self, text='v0.1',font=("JetBrains Mono Medium", 20))
        #self.launch_version_label.grid(row=1, column=0, padx=(670, 10), pady=(370, 0), sticky="w")

        #Создание окна настроек
        self.sett_opened = False
        def settings_win():
            if self.sett_opened == False:
                self.sett_opened = True

                settings_wind = CTk.CTkToplevel(self)

                # получение и расположение окна по центру экрана
                x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 3
                y = (self.winfo_screenheight() - self.winfo_reqheight()) / 3
                settings_wind.wm_geometry("+%d+%d" % (x, y))
                settings_wind.wm_geometry()

                # настройка окна настроек
                settings_wind.geometry("400x300")
                settings_wind.title("Settings")
                settings_wind.after(201, lambda: settings_wind.iconbitmap('images/icon.ico'))
                settings_wind.resizable(False, False)

                # Настройка оперативки
                def ram_choice(choice):
                    self.memory_mb = int(choice)
                    config['Ram_memory'] = {'ram': self.memory_mb}

                self.ram_combobox = CTk.CTkComboBox(settings_wind, width=160, height=35, values=["1024", "2048", "3072", "4096", "5120", "6144", "7168", "8192"], command=ram_choice)
                self.ram_combobox.grid(row=1, column=0, padx=(60, 10), pady=(10, 10), sticky="w")
                self.ram_combobox.set(str(self.memory_mb))

                CTkScrollableDropdown(self.ram_combobox, hover_color='#087301', values=["1024", "2048", "3072", "4096", "5120", "6144", "7168", "8192"], frame_corner_radius=7)

                #Выбор директории
                def Mc_dir_select():
                    select_dir = filedialog.askdirectory()
                    minecraft_dir = "../.minecraft"
                    self.mc_directory = "".join([select_dir, minecraft_dir])
                    self.Dir_lable.configure(text=self.mc_directory)
                    config['Directory'] = {'dir': self.mc_directory}

                self.select_directory_button = CTk.CTkButton(master=settings_wind, width=30, height=35, fg_color='#088f00', hover_color='#087301', corner_radius=13, border_width=0,font=("JetBrains Mono Medium", 15), text="Select Folder", command=lambda: Mc_dir_select())
                self.select_directory_button.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

                #тексты
                #RAM
                self.Ram_lable = CTk.CTkLabel(settings_wind, text="RAM", font=("JetBrains Mono Medium", 25))
                self.Ram_lable.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
                #Директория
                self.Dir_lable = CTk.CTkLabel(settings_wind, text=self.mc_directory, font=("JetBrains Mono Medium", 14))
                self.Dir_lable.grid(row=2, column=0, padx=(160, 10), pady=(10, 10), sticky="w")


                # Защита от повторного открытия окна
                def openedFalse():
                    self.sett_opened = False
                    with open('../saved_variables.ini', 'w') as configfile:
                        config.write(configfile)
                    settings_wind.destroy()
                settings_wind.protocol("WM_DELETE_WINDOW", openedFalse)

if __name__ == "__main__":
    app = App()
    app.mainloop()