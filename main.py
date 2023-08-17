# Importando bibliotecas
import pyautogui
import pytesseract
import cv2
import keyboard
import pystray
import sys
import os
from pyperclip import copy
from PIL import Image
from plyer import notification

# Criando um método que verifica se está aberto em desenvolvimento ou em um executável
# Ele retorna o local apropriado dependendo de onde o aplicativo se encontra
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


# Definindo variáveis de caminhos dinâmicos
screenshot_url = get_resource_path(r"assets/screenshot.png")
image_icon_path = get_resource_path(r"assets/icon.png")


# Criando uma variável de um objeto de Imagem com o caminho selecionado
image_icon = Image.open(image_icon_path)


# Uma classe que referencía a linguagem para qual sera usada no aplicativo
class Language:
    def __init__(self):
        self.actual_language = None

    def change_actual_language(self, new_actual_language):
        self.actual_language = new_actual_language


# instancia da classe que sera usada
app_language = Language()


# método simples para tirar um screenshot da tela inteira do usuário
def screenshot_from_app():
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_url)


# Método que transforma uma imagem em texto usando tesseract
def img_to_string(img_url):
    path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = path
    return pytesseract.image_to_string(img_url, lang=app_language.actual_language)


# Método para recortar a screenshot e usar o método img_to_string() para copiar o texto da imagem
def cut_image():
    try:
        im = cv2.imread(screenshot_url)
        cv2.namedWindow("Select ROI", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Select ROI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        roi = cv2.selectROI("Select ROI", im, showCrosshair=False)
        im_cropped = im[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        cv2.imwrite(screenshot_url, im_cropped)
        image_in_string = img_to_string(screenshot_url)

        if not image_in_string:
            # se der erro ao transformar a imagem em texto (aparece notificação)
            notification.notify(
                title="Erro ao copiar imagem",
                message="Ocorreu um erro ao copiar a imagem, tente novamente (selecione uma imagem com texto)",
                app_name="Shotext",
                app_icon=get_resource_path("favicon.ico"),
                timeout=2,
            )
        else:
            # Copiar string para a área de transferência do usuário
            copy(image_in_string)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Fecha todas as janelas caso der certo ou não
        cv2.destroyAllWindows()


# Método principal que faz a captura de tela, recorta a imagem e copía o texto dela para a área de transferência
def on_press_key():
    screenshot_from_app()
    cut_image()


# Método geral do Menu Icon
def app_handle(icon_app, item):
    if str(item) == "Screenshot":
        on_press_key()
    if str(item) == "Exit":
        icon_app.stop()
        sys.exit()


# Método para mudar a linguagem usada no scanner do aplicativo
def change_language(_, item):
    if str(item) == "Portuguese":
        app_language.change_actual_language("por")
    elif str(item) == "English":
        app_language.change_actual_language("eng")


# Sub-menu de linguagens do pystray
languages_submenu = pystray.Menu(
    pystray.MenuItem("Portuguese", change_language),
    pystray.MenuItem("English", change_language)
)


# Menu principal do pystray
icon = pystray.Icon("Shotext", image_icon, menu=pystray.Menu(
    pystray.MenuItem("Languages", languages_submenu),
    pystray.MenuItem("Screenshot", app_handle),
    pystray.MenuItem("Exit", app_handle)
))

# Atalho para o método principal do aplicativo
keyboard.add_hotkey("ctrl+[", on_press_key)

if __name__ == "__main__":
    icon.run()
