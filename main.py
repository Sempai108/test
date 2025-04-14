from Modules.camera_utils import initialize_camera, capture_image
from Modules.gpio_utils import setup_servo, set_angle, cleanup_gpio
from Modules.image_processing import compute_difference, is_pixel_black_or_white
from Modules.display_utils import initialize_display, display_image
from Modules.image_utils import convert_to_1bit
from PIL import Image
from classes.logger import Logger
from config import config
import cv2

logger = Logger().logger

class SetAngle:
    def __init__(self, pwm):
        self.pwm = pwm

    def set_pwm_angel(self):
        set_angle(self.pwm, 90)
        set_angle(self.pwm, 0)

def yes_or_not(count):
    return 1 if count > 30000 else 0

def destroy_window():
    camera = initialize_camera()
    camera.release()
    cv2.destroyAllWindows()
    cleanup_gpio()


def main():
    camera, display = initialize_camera(), initialize_display()
    pwm1, pwm2 = config.SERVO_PIN1, config.SERVO_PIN2
    try:
        image_path, save_path = config.EYE, config.EYE_CONVERTED
        convert_to_1bit(image_path, save_path)
        display_image(display, save_path)
        capture_image(camera, config.W_IMG)  # Сохранение базового изображения
        while True:
            capture_image(camera, config.W1_IMG)
            compute_difference(config.W_IMG, config.W1_IMG, config.RESULT_IMG)

            # Анализ пикселей
            count, old = 0, 0 # Если не пашет, вынести из try var old
            image = Image.open(config.RESULT_IMG)
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    count += is_pixel_black_or_white(pixel)

            human = yes_or_not(count)
            if old == 1 and human == 1:
                logger.info("PERSON WAS DISCOVERED")
                SetAngle(pwm1).set_pwm_angel()
                SetAngle(pwm2).set_pwm_angel()

                human = 0
            else:
                old = human

            if cv2.waitKey(1) & 0xFF == ord('q'):
                destroy_window()
    except Exception as e:
        logger.error(e, exc_info=True)
    except KeyboardInterrupt:
        logger.info("Прерывание программы...")
        destroy_window()


if __name__ == "__main__":
    main()
