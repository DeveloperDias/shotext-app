import pyautogui
import pytesseract
import cv2
import keyboard
from pyperclip import copy
import pystray
import sys
from PIL import Image
import os
from plyer import notification


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


image_icon_path = get_resource_path(r"assets/icon.png")
image_icon = Image.open(image_icon_path)
screenshot_url = get_resource_path(r"assets/screenshot.png")


class Language:
    def __init__(self):
        self.actual_language = None

    def change_actual_language(self, new_actual_language):
        self.actual_language = new_actual_language


app_language = Language()


def img_to_string():
    image = cv2.imread(screenshot_url)
    path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path
    return pytesseract.image_to_string(image, lang=app_language.actual_language)


def cut_image():
    try:
        im = cv2.imread(screenshot_url)
        cv2.namedWindow("Select ROI", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Select ROI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        roi = cv2.selectROI("Select ROI", im, showCrosshair=False)
        im_cropped = im[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        cv2.imwrite(screenshot_url, im_cropped)
        image_in_string = img_to_string()
        if not image_in_string:
            notification.notify(
                title="Erro ao copiar imagem",
                message="Ocorreu um erro ao copiar a imagem, tente novamente (selecione uma imagem com texto)",
                app_name="Shotext",
                app_icon=get_resource_path("favicon.ico"),
                timeout=2,
                toast=False,
                ticker="teste"
            )
        else:
            copy(image_in_string)
    except Exception as e:
        copy(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()


def screenshot_from_app():
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_url)


def on_press_key():
    screenshot_from_app()
    cut_image()


def app_handle(icon_app, item):
    if str(item) == "Screenshot":
        on_press_key()
    if str(item) == "Exit":
        icon_app.stop()
        sys.exit()


def change_language(_, item):
    if str(item) == "Portuguese":
        app_language.change_actual_language("por")
    elif str(item) == "English":
        app_language.change_actual_language("eng")


languages_submenu = pystray.Menu(
    pystray.MenuItem("Portuguese", change_language),
    pystray.MenuItem("English", change_language)
)

icon = pystray.Icon("Shotext", image_icon, menu=pystray.Menu(
    pystray.MenuItem("Languages", languages_submenu),
    pystray.MenuItem("Screenshot", app_handle),
    pystray.MenuItem("Exit", app_handle)
))

keyboard.add_hotkey("ctrl+[", on_press_key)

if __name__ == "__main__":
    icon.run()
