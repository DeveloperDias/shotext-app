import sys
import os
import tkinter as tk
from tkinter import messagebox
import json
import pytesseract
import keyboard
import pystray
import cv2
import pyautogui
from pyperclip import copy
from PIL import Image
from plyer import notification



def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


class AppConfig:
    def __init__(self):
        self.config_json = get_resource_path("config.json")
        self.is_running_app = False
        self.is_running_shortcut_window = False
        self.icon_title = f"{'Shotext' if not self.get_config_json('title') else self.get_config_json('title')}"

    def set_is_running_shortcut_window(self, state: bool):
        self.is_running_shortcut_window = state
    def get_is_running_shortcut_window(self):
        return self.is_running_shortcut_window

    def set_is_running_app(self, state: bool):
        self.is_running_app = state
    def get_is_running_app(self):
        return self.is_running_app

    def set_config_json(self, content_to_set, new_content):
        try:
            with open(self.config_json, "r") as json_file:
                content = json.load(json_file)
                content[content_to_set] = new_content

            with open(self.config_json, "w") as json_file:
                # indent para formatar o JSON de forma legível
                json.dump(content, json_file, indent=4)
        except Exception as e:
            print(f"Error: trying to set file 'config.json': {str(e)}")

    def get_config_json(self, content_to_get):
        try:
            with open(self.config_json, "r") as json_file:
                content = json.load(json_file)
                return content[content_to_get]
        except Exception as e:
            print(f"Error: trying to get file 'config.json': {str(e)} ")

    def set_icon_title(self, config_json_shortcut, config_json_language):
        self.set_config_json(
            "title",
            f"Shortcut: {config_json_shortcut} , Language: {config_json_language}",
        )
        self.icon_title = self.get_config_json("title")


config = AppConfig()

def create_shortcut_window():
    if not config.get_is_running_shortcut_window():

        config.set_is_running_shortcut_window(True)

        shortcut_window = tk.Tk()
        shortcut_window.resizable(False, False)
        shortcut_window.title("Redefinir Atalhos")

        def on_submit():
            new_shortcut = new_shortcut_entry.get()
            try:
                if new_shortcut == "":
                    messagebox.showwarning("Aviso", "Digite um novo atalho")
                    return
                keyboard.add_hotkey(new_shortcut, on_press_key)
                if new_shortcut:
                    keyboard.remove_hotkey(on_press_key)
                    keyboard.add_hotkey(new_shortcut, on_press_key)
                    config.set_config_json("shortcut", new_shortcut)
                    shortcut_window.destroy()
            except Exception as e:
                messagebox.showwarning("Aviso", "Atalho Desconhecido")
                print(e)

        def on_exit():
            shortcut_window.destroy()
            config.set_is_running_shortcut_window(False)

        shortcut_window.protocol("WM_DELETE_WINDOW", on_exit)
        # Centralizando a janela
        window_width = 200
        window_height = 180
        screen_width = shortcut_window.winfo_screenwidth()
        screen_height = shortcut_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        shortcut_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(shortcut_window, text="New shortcut:")
        label.pack_configure(pady=10)

        new_shortcut_entry = tk.Entry(shortcut_window, width=18)
        new_shortcut_entry.pack_configure(pady=5)

        submit_button = tk.Button(shortcut_window, text="Save", command=on_submit, width=15)
        submit_button.pack_configure(pady=5)

        exit_button = tk.Button(shortcut_window, text="Cancel", command=on_exit, width=15)
        exit_button.pack_configure(pady=0)

        return shortcut_window
    else:
        messagebox.showwarning("Aviso", "Janela em andamento")

def open_shortcut_window():
    shortcut_window = create_shortcut_window()
    try:
        shortcut_window.mainloop()
    except Exception as e:
        print(e)


screenshot_url = get_resource_path(r"assets/screenshot.png")
image_icon_path = get_resource_path(r"assets/icon.png")
image_icon = Image.open(image_icon_path)


def screenshot_from_app():
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_url)


def img_to_string(img_url):
    path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path
    return pytesseract.image_to_string(img_url, lang=config.get_config_json("language"))


def cut_image():
    try:
        actual_print = cv2.imread(screenshot_url)
        cv2.namedWindow("Select ROI", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "Select ROI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )
        roi = cv2.selectROI("Select ROI", actual_print, showCrosshair=False)
        actual_print_cropped = actual_print[
            int(roi[1]) : int(roi[1] + roi[3]), int(roi[0]) : int(roi[0] + roi[2])
        ]
        cv2.imwrite(screenshot_url, actual_print_cropped)
        image_in_string = img_to_string(screenshot_url)

        if config.get_config_json("notifications"):
            if not image_in_string:
                notification.notify(
                    title="Erro ao copiar imagem",
                    message="Ocorreu um erro ao copiar a imagem, tente novamente (selecione uma imagem com texto)",
                    app_name="Shotext",
                    app_icon=get_resource_path("favicon.ico"),
                    timeout=2,
                )
            else:
                notification.notify(
                    title="Copiado para área de transferência",
                    message=image_in_string,
                    app_name="Shotext",
                    app_icon=get_resource_path("favicon.ico"),
                    timeout=2,
                )
        copy(image_in_string)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Fecha todas as janelas caso der certo ou não
        config.set_is_running_app(False)
        cv2.destroyAllWindows()


def on_press_key():
    try:
        if not config.get_is_running_app():
            config.set_is_running_app(True)
            screenshot_from_app()
            cut_image()
        else:
            print("App already running")
    except Exception as e:
        print(e)


# Método geral do Menu Icon


def app_handle(icon_app, item):
    if str(item) == "Screenshot":
        on_press_key()
    if str(item) == "Exit":
        icon_app.stop()
        keyboard.remove_hotkey(on_press_key)
    if str(item) == "Shortcut":
        open_shortcut_window()
        config.set_icon_title(
            config.get_config_json("shortcut"), config.get_config_json("language")
        )
        icon_app.title = config.icon_title


# Método para mudar a linguagem usada no scanner do aplicativo


def change_language(icon_app, item):
    if str(item) == "por":
        config.set_config_json("language", item.text)
        config.set_icon_title(
            config.get_config_json("shortcut"), config.get_config_json("language")
        )
        icon_app.title = config.icon_title
        icon_app.notify("Scanner agora está apto para português", "Linguagem Alterada")
    elif str(item) == "eng":
        config.set_config_json("language", item.text)
        config.set_icon_title(
            config.get_config_json("shortcut"), config.get_config_json("language")
        )
        icon_app.title = config.icon_title
        icon_app.notify("Scanner agora está apto para inglês", "Linguagem Alterada")


def change_notify(_, item):
    if str(item) == "No":
        config.set_config_json("notifications", False)
    if str(item) == "Yes":
        config.set_config_json("notifications", True)


# SUB-MENUS
# LANGUAGES
languages_submenu = pystray.Menu(
    pystray.MenuItem("por", change_language), pystray.MenuItem("eng", change_language)
)

# NOTIFICATIONS
notifications_submenu = pystray.Menu(
    pystray.MenuItem("Yes", change_notify),
    pystray.MenuItem("No", change_notify),
)

# Menu principal do pystray
icon = pystray.Icon(
    "Shotext",
    image_icon,
    title=f"{'Shotext' if config.icon_title == '' else config.icon_title }",
    menu=pystray.Menu(
        pystray.MenuItem(
            "Options",
            pystray.Menu(
                pystray.MenuItem("Languages", languages_submenu),
                pystray.MenuItem("Notifications", notifications_submenu),
                pystray.MenuItem("Shortcut", app_handle),
            ),
        ),
        pystray.MenuItem("Screenshot", app_handle, default=True),
        pystray.MenuItem("Exit", app_handle),
    ),
)

keyboard.add_hotkey(config.get_config_json("shortcut"), on_press_key)
# Atalho para o método principal do aplicativo

if __name__ == "__main__":
    icon.run()
