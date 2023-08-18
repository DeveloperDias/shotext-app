# Importando bibliotecas
import pyautogui
import cv2
import pytesseract
import keyboard
import pystray
import sys
import os
from pyperclip import copy
from PIL import Image
from plyer import notification
import tkinter as tk
from tkinter import messagebox
import json

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)

class app_config:
    def __init__(self):
        self.config_json = get_resource_path("config.json")

    def set_config_json(self, content_to_set, new_content):
        try:
            with open(self.config_json, "r") as json_file:
                content = json.load(json_file)
                content[content_to_set] = new_content

            with open(self.config_json, "w") as json_file:
                json.dump(content, json_file, indent=4)  # indent para formatar o JSON de forma legível
        except Exception as e:
            print(f"Error: trying to set file 'config.json': {str(e)}")

    def get_config_json(self, content_to_get):
        try:
            with open(self.config_json, "r") as json_file:
                content = json.load(json_file)
                return content[content_to_get]
        except Exception as e:
            print(f"Error: trying to get file 'config.json': {str(e)} ")
config = app_config()
def create_shortcut_window():
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

    # Centralizando a janela
    window_width = 200
    window_height = 180
    screen_width = shortcut_window.winfo_screenwidth()
    screen_height = shortcut_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    shortcut_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    label = tk.Label(shortcut_window, text="Digite um novo atalho:")
    label.pack_configure(pady=10)

    new_shortcut_entry = tk.Entry(shortcut_window, width=18)
    new_shortcut_entry.pack_configure(pady=5)

    submit_button = tk.Button(shortcut_window, text="Salvar", command=on_submit, width=15)
    submit_button.pack_configure(pady=5)

    exit_button = tk.Button(shortcut_window, text="Sair", command=on_exit, width=15)
    exit_button.pack_configure(pady=0)
    return shortcut_window
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
        im = cv2.imread(screenshot_url)
        cv2.namedWindow("Select ROI", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Select ROI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        roi = cv2.selectROI("Select ROI", im, showCrosshair=False)
        im_cropped = im[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        cv2.imwrite(screenshot_url, im_cropped)
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
        cv2.destroyAllWindows()
def on_press_key():
    screenshot_from_app()
    cut_image()

# Método geral do Menu Icon
def app_handle(icon_app, item):
    if str(item) == "Screenshot":
        on_press_key()
    if str(item) == "Exit":
        icon_app.stop()
        keyboard.remove_hotkey(on_press_key)
    if str(item) == "Shortcut":
        open_shortcut_window()
        icon_app.title = f"{config.get_config_json('shortcut'), config.get_config_json('language')}"
# Método para mudar a linguagem usada no scanner do aplicativo
def change_language(icon_app, item):
    if str(item) == "por":
        config.set_config_json("language", item.text)
        icon_app.title = f"{config.get_config_json('shortcut'), config.get_config_json('language')}"
        icon_app.notify("Scanner agora está apto para português", "Linguagem Alterada")
    elif str(item) == "eng":
        config.set_config_json("language", item.text)
        icon_app.title = f"{config.get_config_json('shortcut'), config.get_config_json('language')}"
        icon_app.notify("Scanner agora está apto para inglês", "Linguagem Alterada")
def change_notify(icon_app, item):
    if str(item) == "No":
        config.set_config_json("notifications", False)
    elif str(item) == "Yes":
        config.set_config_json("notifications", True)


# SUB-MENUS
    # LANGUAGES
languages_submenu = pystray.Menu(
    pystray.MenuItem("por", change_language),
    pystray.MenuItem("eng", change_language)
)
    # NOTIFICATIONS
notifications_submenu = pystray.Menu(
    pystray.MenuItem("Yes", change_notify),
    pystray.MenuItem("No", change_notify),
)

# Menu principal do pystray
icon = pystray.Icon("Shotext", image_icon, title=f"{config.get_config_json('shortcut')} {config.get_config_json('language') if config.get_config_json('language') else 'Escolha um idioma de scanner'}", menu=pystray.Menu(
    pystray.MenuItem("Options", pystray.Menu(
        pystray.MenuItem("Languages", languages_submenu),
        pystray.MenuItem("Notifications", notifications_submenu),
        pystray.MenuItem("Shortcut", app_handle)
    )),
    pystray.MenuItem("Screenshot", app_handle, default=True),
    pystray.MenuItem("Exit", app_handle)
))

keyboard.add_hotkey(config.get_config_json("shortcut"), on_press_key)
# Atalho para o método principal do aplicativo


if __name__ == "__main__":
    icon.run()
