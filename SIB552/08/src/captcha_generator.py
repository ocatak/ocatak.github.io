from io import BytesIO
from captcha.image import ImageCaptcha
import random,string

image = ImageCaptcha()

for i in range(10):
    s = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
    image.write(s, str(i) + '.png')