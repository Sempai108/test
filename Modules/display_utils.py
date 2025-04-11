import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image

def initialize_display(width=128, height=64, i2c_addr=0x3C):
    """
    Инициализация OLED-дисплея SSD1306 через I2C.
    :param width: Ширина дисплея.
    :param height: Высота дисплея.
    :param i2c_addr: Адрес I2C дисплея.
    :return: Объект дисплея.
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    display = SSD1306_I2C(width, height, i2c, addr=i2c_addr)
    display.fill(0)
    display.show()
    return display

def display_image(display, image_path):
    """
    Загружает и отображает изображение на OLED-дисплее.
    :param display: Объект дисплея.
    :param image_path: Путь к изображению.
    """
    image = Image.open(image_path).convert("1")  # Конвертация изображения в чёрно-белый формат (1-bit)
    display.image(image)
    display.show()
