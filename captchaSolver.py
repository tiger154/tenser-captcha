from captcha_solver import CaptchaSolver

CAPTCHA_IMAGE_FOLDER = "target_captcha_images"

solver = CaptchaSolver('browser')
#raw_data = open(CAPTCHA_IMAGE_FOLDER + '/2A2X.png', 'rb').read()
raw_data = open(CAPTCHA_IMAGE_FOLDER + '/300026.png', 'rb').read()
#raw_data = open(CAPTCHA_IMAGE_FOLDER + '/NSI5X4.png', 'rb').read()
print(solver.solve_captcha(raw_data))
