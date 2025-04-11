from Modules.camera_utils import initialize_camera, capture_image
from Modules.gpio_utils import setup_servo, set_angle, cleanup_gpio
from Modules.image_processing import compute_difference, is_pixel_black_or_white
from PIL import Image
from classes.logger import Logger
from config import config
import cv2

logger = Logger().logger

def yes_or_not(count):
    return 1 if count > 30000 else 0


def main():
    camera = initialize_camera()
    pwm1 = config.SERVO_PIN1
    pwm2 = config.SERVO_PIN2

    try:
        capture_image(camera, config.W_IMG)  # Сохранение базового изображения
        old = 0
        while True:
            capture_image(camera, config.W1_IMG)
            compute_difference(config.W_IMG, config.W1_IMG, config.RESULT_IMG)

            # Анализ пикселей
            count = 0
            image = Image.open(config.RESULT_IMG)
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    count += is_pixel_black_or_white(pixel)

            human = yes_or_not(count)
            if old == 1 and human == 1:
                logger.info("PERSON WAS DISCOVERED")
                set_angle(pwm1, 90)
                set_angle(pwm1, 0)
                set_angle(pwm2, 90)
                set_angle(pwm2, 0)
                human = 0
            else:
                old = human

            if cv2.waitKey(1) & 0xFF == ord('q'):
                camera.release()
                cv2.destroyAllWindows()
                cleanup_gpio()
    except Exception as e:
        logger.error(e, exc_info=True)
    except KeyboardInterrupt:
        logger.info("Прерывание программы...")
        camera.release()
        cv2.destroyAllWindows()
        cleanup_gpio()



if __name__ == "__main__":
    main()
