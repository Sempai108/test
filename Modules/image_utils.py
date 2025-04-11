from PIL import Image
from classes.logger import Logger

logger = Logger().logger

def convert_to_1bit(image_path, save_path):
    """
    Конвертирует изображение в чёрно-белый формат (1-bit).
    :param image_path: Путь к исходному изображению.
    :param save_path: Путь для сохранения преобразованного изображения.
    """
    image = Image.open(image_path)
    image = image.convert("1")  # Преобразование в 1-bit формат
    image.save(save_path)
    logger.info(f"Изображение сохранено в {save_path}")
