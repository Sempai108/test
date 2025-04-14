from Modules.gpio_utils import setup_servo
import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

class Config:
    @staticmethod
    def load_config():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            cfg = json.load(file)
            return cfg

    @staticmethod
    def config():
        cfg = Config.load_config()

        nums = cfg.get('count') # 0
        result_img = cfg['images'].get('result') # 1
        w_img = cfg['images'].get('w') # 2
        w1_img = cfg['images'].get('w1') # 3
        eye_img = cfg['images'].get('eye') # 4
        eye_converted_img = cfg['images'].get('eye_converted') # 5

        pin_1 = cfg['pins'].get('SERVO_PIN1') # 6
        pin_2 = cfg['pins'].get('SERVO_PIN2') # 7

        return nums, result_img, w_img, w1_img, eye_img, eye_converted_img, pin_1, pin_2

count = Config.config()[0]
RESULT_IMG = Config.config()[1]
W_IMG = Config.config()[2]
W1_IMG = Config.config()[3]
EYE = Config.config()[4]
EYE_CONVERTED = Config.config()[5]
SERVO_PIN1 = setup_servo(Config.config()[5])
SERVO_PIN2 = setup_servo(Config.config()[7])

