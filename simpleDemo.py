from PIL import Image
import cv2 as cv
import pytesseract
import os

CAPTCHA_IMAGE_FOLDER = "target_captcha_images"

print(CAPTCHA_IMAGE_FOLDER)


# load the example image and convert it to grayscale
#image = cv.imread(CAPTCHA_IMAGE_FOLDER + '/NSI5X4.png')
image = cv.imread(CAPTCHA_IMAGE_FOLDER + '/300026.png')
#image = cv.imread(CAPTCHA_IMAGE_FOLDER + '/2A2X.png')
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# thresholding to preprocess the image
gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

# median blurring should be done to remove noise
#gray = cv.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file so we can apply OCR to it
filename = "{}.png".format(os.getpid())
cv.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
text = pytesseract.image_to_string(Image.open(filename), config='psm 6')
os.remove(filename)

print(text)




# test simple
# import tensorflow as tf
# hello = tf.constant("Hello Tensorflow")
# sess = tf.Session()
# print(sess.run(hello))
