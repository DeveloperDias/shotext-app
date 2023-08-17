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
language = "por"


def img_to_string():
    image = cv2.imread(screenshot_url)
    path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path
    return pytesseract.image_to_string(image, lang=language)


def error_notification(title, message, app_name, icon_path, timeout):
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        app_icon=icon_path,
        timeout=timeout
    )


def cut_image():
    try:
        im = cv2.imread(screenshot_url)
        cv2.namedWindow("Select ROI", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Select ROI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        roi = cv2.selectROI("Select ROI", im, showCrosshair=False)
        im_cropped = im[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        cv2.imwrite(screenshot_url, im_cropped)
        image_in_string = img_to_string()
        if image_in_string == "":
            error_notification(
                "Erro ao copiar imagem",
                "Ocorreu um erro ao copiar a imagem, tente novamente (selecione uma imagem com texto)",
                "Shotext",
                "favicon.ico",
                2
            )
        else:
            copy(image_in_string)
    except Exception as e:
        print(f"Error: {e}")
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
    elif str(item) == "Exit":
        icon_app.stop()
        sys.exit()


def change_language(_, item):
    global language
    if str(item) == "pt-br":
        language = "pt-br"
    elif str(item) == "eng":
        language = "eng"


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
icon.run()
