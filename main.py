from camera_utils import initialize_camera, capture_image
from gpio_utils import setup_servo, set_angle, cleanup_gpio
from image_processing import compute_difference, is_pixel_black_or_white
from PIL import Image
import config
import cv2


def yes_or_not(count):
    return 1 if count > 30000 else 0


def main():
    camera = initialize_camera()
    pwm1 = setup_servo(config.servo_pin1)
    pwm2 = setup_servo(config.servo_pin2)

    try:
        capture_image(camera, "w.png")  # Сохранение базового изображения
        old = 0
        while True:
            capture_image(camera, "w1.png")
            compute_difference("w.png", "w1.png", "result.jpg")

            # Анализ пикселей
            count = 0
            image = Image.open('result.jpg')
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    count += is_pixel_black_or_white(pixel)

            human = yes_or_not(count)
            if old == 1 and human == 1:
                print("PERSON WAS DISCOVERED")
                set_angle(pwm1, 90)
                set_angle(pwm1, 0)
                set_angle(pwm2, 90)
                set_angle(pwm2, 0)
                human = 0
            else:
                old = human

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Прерывание программы...")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        cleanup_gpio()


if __name__ == "__main__":
    main()
